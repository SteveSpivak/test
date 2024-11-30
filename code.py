public class Script : ScriptBase
{
    public override async Task<HttpResponseMessage> ExecuteAsync()
    {
        // Check if the operation ID matches what is specified in the OpenAPI definition
        if (this.Context.OperationId == "ParseSingleVariable")
        {
            return await this.HandleParseOperation().ConfigureAwait(false);
        }
        
        // Handle invalid operation ID
        HttpResponseMessage response = new HttpResponseMessage(HttpStatusCode.BadRequest);
        response.Content = CreateJsonContent($"Unknown operation ID '{this.Context.OperationId}'");
        return response;
    }

    private async Task<HttpResponseMessage> HandleParseOperation()
    {
        // Read and parse the JSON input
        var contentAsString = await this.Context.Request.Content.ReadAsStringAsync().ConfigureAwait(false);
        var contentAsJson = JObject.Parse(contentAsString);

        try
        {
            // Get the variable text from the input JSON
            string variableText = (string)contentAsJson["variableText"];
            
            // Extract variable name
            string variableName = ExtractBetween(variableText, "variable \"", "\" {");
            
            // Extract content block
            string contentBlock = ExtractBetween(variableText, "{", "}");
            
            // Parse the content block into a JObject
            var contentAsJObject = new JObject();
            string[] lines = contentBlock.Split(new[] { '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
            
            foreach (var line in lines)
            {
                string trimmedLine = line.Trim();
                if (string.IsNullOrEmpty(trimmedLine) || trimmedLine.StartsWith("#"))
                    continue;

                string[] parts = trimmedLine.Split('=');
                if (parts.Length == 2)
                {
                    string key = parts[0].Trim();
                    string value = parts[1].Trim();
                    contentAsJObject[key] = value;
                }
            }

            // Create the output JSON
            JObject output = new JObject
            {
                [variableName] = contentAsJObject
            };

            // Return success response
            var response = new HttpResponseMessage(HttpStatusCode.OK);
            response.Content = CreateJsonContent(output.ToString());
            return response;
        }
        catch (Exception ex)
        {
            // Return error response
            var response = new HttpResponseMessage(HttpStatusCode.BadRequest);
            response.Content = CreateJsonContent($"Error parsing variable: {ex.Message}");
            return response;
        }
    }

    private string ExtractBetween(string text, string start, string end)
    {
        int startIndex = text.IndexOf(start) + start.Length;
        int endIndex = text.IndexOf(end, startIndex);
        return text.Substring(startIndex, endIndex - startIndex).Trim();
    }
}
