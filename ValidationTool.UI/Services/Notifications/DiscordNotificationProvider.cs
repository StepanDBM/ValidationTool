/*using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;
using ValidationTool.Services.Notifications;

namespace ValidationTool.UI.Services.Notifications {
    public class DiscordNotificationProvider : INotificationProvider {
        public string Name => "Discord";

        private readonly HttpClient _httpClient;
        private readonly string _botToken;
        public DiscordNotificationProvider(HttpClient httpClient, string botToken) {
            _httpClient = httpClient;
            _botToken = botToken;
        }

        public async Task SendAsync(NotificationMessage message) {
            var dmChannel = OpenDmChannel(message.RecipientId);
            await PostMessage(dmChannel, message);
        }

        private async Task<string> OpenDmChannel(string userID) {

        }
        private async Task PostMessage(string dmChannel, string message) {

        }
    }
}
*/