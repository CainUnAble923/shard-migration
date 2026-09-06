using System;
using System.Collections.Generic;
using System.IO;
using System.Text;
using System.Xml;
using Server.Accounting;
using Server.Accounting.Security;

namespace Server.Commands;

/// <summary>
/// Temporary migration command for exporting ModernUO accounts in ServUO's XML shape.
/// Copy this file into a ModernUO UOContent source directory, rebuild, then run
/// [ExportServUOAccounts. The command refuses to export until every account uses SHA2.
/// </summary>
public static class ExportServUOAccounts
{
    private static readonly string OutputPath = Path.Combine("Export", "ServUO", "accounts.xml");

    public static void Configure()
    {
        CommandSystem.Register("ExportServUOAccounts", AccessLevel.Owner, Export_OnCommand);
    }

    [Usage("ExportServUOAccounts")]
    [Description("Exports SHA2 accounts to Export/ServUO/accounts.xml for ServUO pub57.")]
    private static void Export_OnCommand(CommandEventArgs e)
    {
        var accounts = new List<Account>();
        var incompatible = 0;

        foreach (var candidate in Accounts.GetAccounts())
        {
            if (candidate is not Account account || account.Deleted)
            {
                continue;
            }

            accounts.Add(account);
            if (!HasCompatiblePassword(account))
            {
                incompatible++;
            }
        }

        if (incompatible != 0)
        {
            e.Mobile.SendMessage(
                0x22,
                $"Export refused: {incompatible} account(s) do not have a valid SHA2 password hash."
            );
            e.Mobile.SendMessage(
                0x22,
                "Set accountSecurity.encryptionAlgorithm to SHA2 and let those users log in before retrying."
            );
            return;
        }

        accounts.Sort((left, right) => string.CompareOrdinal(left.Username, right.Username));

        try
        {
            var directory = Path.GetDirectoryName(OutputPath);
            Directory.CreateDirectory(directory!);

            var temporaryPath = $"{OutputPath}.{Guid.NewGuid():N}.tmp";
            try
            {
                WriteAccounts(temporaryPath, accounts);
                File.Move(temporaryPath, OutputPath, true);
            }
            finally
            {
                File.Delete(temporaryPath);
            }

            e.Mobile.SendMessage($"Exported {accounts.Count} account(s) to {OutputPath}.");
            e.Mobile.SendMessage(
                0x35,
                "The file contains password hashes, IP addresses, comments, and email addresses. Protect it as a secret."
            );
        }
        catch (Exception exception)
        {
            e.Mobile.SendMessage(0x22, $"Account export failed: {exception.Message}");
        }
    }

    private static bool HasCompatiblePassword(Account account)
    {
        if (account.PasswordAlgorithm != PasswordProtectionAlgorithm.SHA2 || account.Password?.Length != 128)
        {
            return false;
        }

        for (var i = 0; i < account.Password.Length; i++)
        {
            if (!Uri.IsHexDigit(account.Password[i]))
            {
                return false;
            }
        }

        return true;
    }

    private static void WriteAccounts(string path, List<Account> accounts)
    {
        var settings = new XmlWriterSettings
        {
            Encoding = new UTF8Encoding(false),
            Indent = true,
            IndentChars = "\t"
        };

        using var xml = XmlWriter.Create(path, settings);
        xml.WriteStartDocument(true);
        xml.WriteStartElement("accounts");
        xml.WriteAttributeString("count", XmlConvert.ToString(accounts.Count));

        for (var i = 0; i < accounts.Count; i++)
        {
            WriteAccount(xml, accounts[i]);
        }

        xml.WriteEndElement();
        xml.WriteEndDocument();
    }

    private static void WriteAccount(XmlWriter xml, Account account)
    {
        xml.WriteStartElement("account");
        xml.WriteElementString("username", account.Username);
        xml.WriteElementString("newSecureCryptPassword", HyphenateSha512(account.Password));

        if (account.AccessLevel >= AccessLevel.Counselor)
        {
            xml.WriteElementString("accessLevel", account.AccessLevel.ToString());
        }

        if (account.Flags != 0)
        {
            xml.WriteElementString("flags", XmlConvert.ToString(account.Flags));
        }

        xml.WriteElementString("created", XmlConvert.ToString(account.Created, XmlDateTimeSerializationMode.Utc));
        xml.WriteElementString("lastLogin", XmlConvert.ToString(account.LastLogin, XmlDateTimeSerializationMode.Utc));
        xml.WriteElementString("totalGameTime", XmlConvert.ToString(account.TotalGameTime));
        WriteCharacters(xml, account);
        WriteComments(xml, account);
        WriteTags(xml, account);
        WriteAddresses(xml, account);

        var currency = account.TotalPlat + account.TotalGold / (double)AccountGold.CurrencyThreshold;
        xml.WriteElementString("totalCurrency", XmlConvert.ToString(currency));
        xml.WriteElementString("sovereigns", "0");

        // Stock ServUO pub57 ignores these extension elements. A target-side loader
        // patch can consume them without losing data through TotalCurrency's double.
        xml.WriteElementString("modernUOEmail", account.Email ?? string.Empty);
        xml.WriteElementString("modernUOTotalGold", XmlConvert.ToString(account.TotalGold));
        xml.WriteElementString("modernUOTotalPlat", XmlConvert.ToString(account.TotalPlat));
        xml.WriteEndElement();
    }

    private static void WriteCharacters(XmlWriter xml, Account account)
    {
        xml.WriteStartElement("chars");
        for (var i = 0; i < account.Length; i++)
        {
            var mobile = account[i];
            if (mobile == null || mobile.Deleted)
            {
                continue;
            }

            xml.WriteStartElement("char");
            xml.WriteAttributeString("index", XmlConvert.ToString(i));
            xml.WriteString(XmlConvert.ToString(mobile.Serial.Value));
            xml.WriteEndElement();
        }
        xml.WriteEndElement();
    }

    private static void WriteComments(XmlWriter xml, Account account)
    {
        if (account.Comments.Count == 0)
        {
            return;
        }

        xml.WriteStartElement("comments");
        for (var i = 0; i < account.Comments.Count; i++)
        {
            var comment = account.Comments[i];
            xml.WriteStartElement("comment");
            xml.WriteAttributeString("addedBy", comment.AddedBy);
            xml.WriteAttributeString(
                "lastModified",
                XmlConvert.ToString(comment.LastModified, XmlDateTimeSerializationMode.Utc)
            );
            xml.WriteString(comment.Content ?? string.Empty);
            xml.WriteEndElement();
        }
        xml.WriteEndElement();
    }

    private static void WriteTags(XmlWriter xml, Account account)
    {
        if (account.Tags.Count == 0)
        {
            return;
        }

        xml.WriteStartElement("tags");
        for (var i = 0; i < account.Tags.Count; i++)
        {
            var tag = account.Tags[i];
            xml.WriteStartElement("tag");
            xml.WriteAttributeString("name", tag.Name);
            xml.WriteString(tag.Value ?? string.Empty);
            xml.WriteEndElement();
        }
        xml.WriteEndElement();
    }

    private static void WriteAddresses(XmlWriter xml, Account account)
    {
        if (account.LoginIPs.Length == 0)
        {
            return;
        }

        xml.WriteStartElement("addressList");
        xml.WriteAttributeString("count", XmlConvert.ToString(account.LoginIPs.Length));
        for (var i = 0; i < account.LoginIPs.Length; i++)
        {
            xml.WriteElementString("ip", account.LoginIPs[i].ToString());
        }
        xml.WriteEndElement();
    }

    private static string HyphenateSha512(string hash)
    {
        return string.Create(191, hash, static (destination, source) =>
        {
            var destinationIndex = 0;
            for (var sourceIndex = 0; sourceIndex < source.Length; sourceIndex++)
            {
                if (sourceIndex != 0 && sourceIndex % 2 == 0)
                {
                    destination[destinationIndex++] = '-';
                }
                destination[destinationIndex++] = char.ToUpperInvariant(source[sourceIndex]);
            }
        });
    }
}
