using System;
using System.Net;
using System.Net.Http;
using System.Threading.Tasks;
using Newtonsoft.Json.Linq;

public class Script : ScriptBase
{
    public override async Task<HttpResponseMessage> ExecuteAsync()
    {
        // Check the operation ID
        if (this.Context.OperationId == "ParseSingleVariable")
        {
            return await this.ParseVariable().ConfigureAwait(false);
        }

        // Handle invalid operation ID
        HttpResponseMessage response = new HttpResponseMessage(HttpStatusCode.BadRequest);
        response.Content = CreateJsonContent($"Unknown operation ID '{this.Context.OperationId}'");
        return response;
    }

    private async Task<HttpResponseMessage> ParseVariable()
    {
        HttpResponseMessage response;

        // Read the incoming content (Terraform variable text)
        var contentAsString = await this.Context.Request.Content.ReadAsStringAsync().ConfigureAwait(false);

        try
        {
            // Call the function to transform the variable block into JSON
            string jsonOutput = ConvertVariableToJson(contentAsString);

            // Create a success response with the JSON output
            response = new HttpResponseMessage(HttpStatusCode.OK);
            response.Content = CreateJsonContent(jsonOutput);
            return response;
        }
        catch (Exception ex)
        {
            // Handle errors
            response = new HttpResponseMessage(HttpStatusCode.InternalServerError);
            response.Content = CreateJsonContent($"Error: {ex.Message}");
            return response;
        }
    }

    private string ConvertVariableToJson(string variableText)
    {
        try
        {
            // Clean up input and split the text into manageable parts
            variableText = variableText.Trim();

            // Find the variable name using basic string operations
            string variableName = ExtractBetween(variableText, "variable \"", "\" {");

            // Find the content block within the variable definition
            string contentBlock = ExtractBetween(variableText, "{", "}");

            // Parse the content block into key-value pairs
            var contentAsJson = new JObject();
            string[] lines = contentBlock.Split(new[] { '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);

            foreach (var line in lines)
            {
                // Skip comments or empty lines
                if (line.Trim().StartsWith("#") || string.IsNullOrWhiteSpace(line))
                    continue;

                // Extract key-value pairs
                string[] parts = line.Split('=');
                if (parts.Length == 2)
                {
                    string key = parts[0].Trim();
                    string value = parts[1].Trim();

                    // Handle optional fields and their types
                    if (value.StartsWith("optional("))
                    {
                        value = ExtractBetween(value, "optional(", ")");
                    }
                    else if (value.StartsWith("list(") || value.StartsWith("map(") || value.StartsWith("object("))
                    {
                        value = "complex type"; // Placeholder for complex types
                    }

                    // Add the key-value pair to the JSON object
                    contentAsJson[key] = value;
                }
            }

            // Wrap the variable name and content into a JSON structure
            var result = new JObject
            {
                [variableName] = contentAsJson
            };

            return result.ToString(Newtonsoft.Json.Formatting.Indented);
        }
        catch (Exception ex)
        {
            throw new Exception($"Error while parsing variable: {ex.Message}");
        }
    }

    private string ExtractBetween(string text, string start, string end)
    {
        int startIndex = text.IndexOf(start) + start.Length;
        int endIndex = text.IndexOf(end, startIndex);
        return text.Substring(startIndex, endIndex - startIndex).Trim();
    }

    private HttpContent CreateJsonContent(string content)
    {
        return new StringContent(content, System.Text.Encoding.UTF8, "application/json");
    }
}
