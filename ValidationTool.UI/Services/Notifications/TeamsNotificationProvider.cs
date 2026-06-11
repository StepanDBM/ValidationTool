using System;
using System.Net.Http;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;

namespace ValidationTool.Services.Notifications {
    public class TeamsNotificationProvider : INotificationProvider {
        public string Name => "Teams";

        private readonly HttpClient _httpClient;
        private readonly string _webhookUrl;

        public TeamsNotificationProvider(HttpClient httpClient, string webhookUrl) {
            _httpClient = httpClient;
            _webhookUrl = webhookUrl;
        }

        public async Task SendAsync(NotificationMessage message) {
            var payload = BuildPayload(message);

            var content = new StringContent(
                JsonSerializer.Serialize(payload),
                Encoding.UTF8,
                "application/json"
            );

            var response = await _httpClient.PostAsync(_webhookUrl, content);

            if (!response.IsSuccessStatusCode) {
                var body = await response.Content.ReadAsStringAsync();
                throw new Exception($"Teams notification failed: {response.StatusCode} - {body}");
            }
        }

        private object BuildPayload(NotificationMessage message) {
            return new {
                @type = "MessageCard",
                @context = "https://schema.org/extensions",
                summary = message.Title,
                themeColor = "FF0000",
                title = message.Title,
                text = message.Body
            };
        }
    }
}