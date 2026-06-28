using System;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;

namespace ValidationTool.Services.Notifications {
    public class SlackDmNotificationProvider : INotificationProvider {
        public string Name => "Slack";

        private readonly HttpClient _httpClient;
        private readonly string _botToken;

        public SlackDmNotificationProvider(HttpClient httpClient, string botToken) {
            _httpClient = httpClient;
            _botToken = botToken;
        }

        public async Task SendAsync(NotificationMessage message){

            var slackUserId = await GetUserIdByEmail(message.RecipientId);
            var dmChannel = await OpenDmChannel(slackUserId);

            await PostMessage(dmChannel, message);
        }

        private async Task<string> OpenDmChannel(string userId) {

            var request = new HttpRequestMessage(
                HttpMethod.Post,
                "https://slack.com/api/conversations.open"
            );

            request.Headers.Authorization =
                new AuthenticationHeaderValue("Bearer", _botToken);

            request.Content = new StringContent(
                JsonSerializer.Serialize(new { users = userId }),
                Encoding.UTF8,
                "application/json"
            );

            var response = await _httpClient.SendAsync(request);
            var json = await response.Content.ReadAsStringAsync();


            using (var doc = JsonDocument.Parse(json)) {
                var root = doc.RootElement;

                if (!root.TryGetProperty("ok", out var okProp) || !okProp.GetBoolean())
                    throw new Exception($"Slack OpenDmChannel failed: {json}");

                if (!root.TryGetProperty("channel", out var channelElement) ||
                    !channelElement.TryGetProperty("id", out var idElement))
                    throw new Exception($"Slack missing channel id: {json}");

                return idElement.GetString();
            }
        }

        private async Task PostMessage(string channelId, NotificationMessage message) {
            var request = new HttpRequestMessage(
                HttpMethod.Post,
                "https://slack.com/api/chat.postMessage"
            );

            request.Headers.Authorization =
                new AuthenticationHeaderValue("Bearer", _botToken);

            request.Content = new StringContent(
                JsonSerializer.Serialize(new {
                    channel = channelId,
                    text = $"*{message.Title}*\n{message.Body}"
                }),
                Encoding.UTF8,
                "application/json"
            );
            var response = await _httpClient.SendAsync(request);
            var json = await response.Content.ReadAsStringAsync();

            Console.WriteLine("[Slack] chat.postMessage response:");
            Console.WriteLine(json);

            if (!response.IsSuccessStatusCode) {
                throw new Exception($"Slack HTTP error: {response.StatusCode} - {json}");
            }

            using (var doc = JsonDocument.Parse(json)) {
                var root = doc.RootElement;

                if (root.TryGetProperty("ok", out var okProp) && okProp.ValueKind == JsonValueKind.False) {
                    var error = root.TryGetProperty("error", out var err)
                        ? err.GetString()
                        : "unknown_error";

                    throw new Exception($"Slack API error: {error} - {json}");
                }
            }
        }

        private async Task<string> GetUserIdByEmail(string email) {
            var request = new HttpRequestMessage(
                HttpMethod.Get,
                $"https://slack.com/api/users.lookupByEmail?email={Uri.EscapeDataString(email)}"
            );

            request.Headers.Authorization =
                new AuthenticationHeaderValue("Bearer", _botToken);

            var response = await _httpClient.SendAsync(request);
            var json = await response.Content.ReadAsStringAsync();

            using (var doc = JsonDocument.Parse(json)) {
                var root = doc.RootElement;

                if (!root.TryGetProperty("user", out var userElement) ||
                    !userElement.TryGetProperty("id", out var idElement)) {
                    throw new Exception($"Slack lookupByEmail failed: {json}");
                }

                return idElement.GetString();
            }
        }
        private void Dump(string title, string json) {
            Console.WriteLine("==================================");
            Console.WriteLine(title);
            Console.WriteLine(json);
            Console.WriteLine("==================================");
        }
    }
}