using System;
using System.Net;
using System.Net.Http;
using System.Threading.Tasks;
using Newtonsoft.Json.Linq;

public class Script : ScriptBase
{
    public override async Task<HttpResponseMessage> ExecuteAsync()
    {
        if (this.Context.OperationId != "ParseSingleVariable")
        {
            return new HttpResponseMessage(HttpStatusCode.BadRequest)
            {
                Content = CreateJsonContent($"Unknown operation ID '{this.Context.OperationId}'")
            };
        }

        // Read and validate the JSON input
        try
        {
            var requestContent = await this.Context.Request.Content.ReadAsStringAsync().ConfigureAwait(false);
            var jsonRequest = JObject.Parse(requestContent);
            
            if (!jsonRequest.ContainsKey("variableText"))
            {
                return new HttpResponseMessage(HttpStatusCode.BadRequest)
                {
                    Content = CreateJsonContent("Missing required 'variableText' field in request")
                };
            }

            string variableText = jsonRequest["variableText"].ToString();
            string jsonOutput = ConvertVariableToJson(variableText);

            return new HttpResponseMessage(HttpStatusCode.OK)
            {
                Content = CreateJsonContent(jsonOutput)
            };
        }
        catch (JsonReaderException ex)
        {
            return new HttpResponseMessage(HttpStatusCode.BadRequest)
            {
                Content = CreateJsonContent($"Invalid JSON in request: {ex.Message}")
            };
        }
        catch (Exception ex)
        {
            return new HttpResponseMessage(HttpStatusCode.InternalServerError)
            {
                Content = CreateJsonContent($"Error processing request: {ex.Message}")
            };
        }
    }

    private string ConvertVariableToJson(string variableText)
    {
        try
        {
            variableText = variableText.Trim();
            
            // Enhanced variable name extraction with validation
            string variableName = ExtractVariableName(variableText);
            if (string.IsNullOrEmpty(variableName))
            {
                throw new Exception("Could not extract variable name");
            }

            // Extract and parse the content block
            string contentBlock = ExtractBetween(variableText, "{", "}");
            var contentAsJson = ParseVariableContent(contentBlock);

            return new JObject
            {
                [variableName] = contentAsJson
            }.ToString(Newtonsoft.Json.Formatting.Indented);
        }
        catch (Exception ex)
        {
            throw new Exception($"Error parsing Terraform variable: {ex.Message}");
        }
    }

    private string ExtractVariableName(string text)
    {
        var match = System.Text.RegularExpressions.Regex.Match(
            text,
            @"variable\s+""([^""]+)""");
        
        return match.Success ? match.Groups[1].Value : string.Empty;
    }

    private JObject ParseVariableContent(string content)
    {
        var result = new JObject();
        var lines = content.Split(new[] { '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries)
            .Select(l => l.Trim())
            .Where(l => !string.IsNullOrEmpty(l) && !l.StartsWith("#"));

        foreach (var line in lines)
        {
            var parts = line.Split(new[] { '=' }, 2);
            if (parts.Length != 2) continue;

            string key = parts[0].Trim();
            string value = parts[1].Trim();

            // Handle special types
            if (value.StartsWith("optional("))
            {
                value = ExtractBetween(value, "optional(", ")");
            }
            else if (value.StartsWith("list(") || 
                     value.StartsWith("map(") || 
                     value.StartsWith("object("))
            {
                value = "complex_type";
            }

            result[key] = value;
        }

        return result;
    }

    private string ExtractBetween(string text, string start, string end)
    {
        int startIndex = text.IndexOf(start);
        if (startIndex == -1) return string.Empty;
        
        startIndex += start.Length;
        int endIndex = text.IndexOf(end, startIndex);
        if (endIndex == -1) return string.Empty;
        
        return text.Substring(startIndex, endIndex - startIndex).Trim();
    }

    private HttpContent CreateJsonContent(string content)
    {
        return new StringContent(
            content,
            System.Text.Encoding.UTF8,
            "application/json"
        );
    }
}
