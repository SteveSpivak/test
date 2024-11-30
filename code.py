using System;
using System.Collections.Generic;
using System.Text.RegularExpressions;
using Newtonsoft.Json;

public static class Script
{
    public static string Transform(string terraformVariables)
    {
        try
        {
            // Prepare the output dictionary to hold parsed variables
            var result = new Dictionary<string, object>();

            // Use a regex to identify variable blocks
            string variablePattern = @"variable\s+""(?<name>[^""]+)""\s*{(?<content>[\s\S]*?)}";
            var variableMatches = Regex.Matches(terraformVariables, variablePattern);

            foreach (Match match in variableMatches)
            {
                string variableName = match.Groups["name"].Value;
                string variableContent = match.Groups["content"].Value;

                // Parse each variable's content into a dictionary
                var variableDetails = new Dictionary<string, object>();

                // Match individual key-value pairs within the variable block
                string keyValuePattern = @"(?<key>\w+)\s*=\s*(?<value>.+)";
                var keyValueMatches = Regex.Matches(variableContent, keyValuePattern);

                foreach (Match keyValueMatch in keyValueMatches)
                {
                    string key = keyValueMatch.Groups["key"].Value.Trim();
                    string value = keyValueMatch.Groups["value"].Value.Trim();

                    // Handle different data types (string, list, boolean, etc.)
                    if (value.StartsWith("\"") && value.EndsWith("\""))
                    {
                        // Remove quotes for string values
                        value = value.Trim('"');
                        variableDetails[key] = value;
                    }
                    else if (value.StartsWith("[") && value.EndsWith("]"))
                    {
                        // Convert list values into an array
                        value = value.Trim('[', ']');
                        variableDetails[key] = value.Split(',');
                    }
                    else if (value.Equals("true", StringComparison.OrdinalIgnoreCase) || value.Equals("false", StringComparison.OrdinalIgnoreCase))
                    {
                        // Handle boolean values
                        variableDetails[key] = bool.Parse(value);
                    }
                    else if (int.TryParse(value, out int intValue))
                    {
                        // Handle integer values
                        variableDetails[key] = intValue;
                    }
                    else
                    {
                        // Default to treating the value as a string
                        variableDetails[key] = value;
                    }
                }

                // Add the parsed variable to the result dictionary
                result[variableName] = variableDetails;
            }

            // Convert the result to a JSON string
            return JsonConvert.SerializeObject(result, Formatting.Indented);
        }
        catch (Exception ex)
        {
            return $"Error: {ex.Message}";
        }
    }
}
