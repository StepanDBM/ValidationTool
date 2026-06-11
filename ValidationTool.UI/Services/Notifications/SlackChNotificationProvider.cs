using System;
using System.Net.Http;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;

namespace ValidationTool.Services.Notifications {
    public class SlackChNotificationProvider : INotificationProvider {
        public string Name => "Slack";

        private readonly HttpClient _httpClient;
        private readonly string _webhookUrl;

        public SlackChNotificationProvider(HttpClient httpClient, string webhookUrl) {
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
                throw new Exception($"Slack notification failed: {response.StatusCode} - {body}");
            }
        }

        private object BuildPayload(NotificationMessage message) {
            return new {
                text = $"*{message.Title}*\n{message.Body}",
                // Optional: if you later map RecipientId -> Slack user
                // channel / user mention logic goes here
            };
        }
    }
}