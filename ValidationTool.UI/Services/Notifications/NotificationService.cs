using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;
using System.Net.Http;
using System.Threading.Tasks;
using ValidationTool.UI.ViewModels;

namespace ValidationTool.Services.Notifications {
    public class NotificationService {
        private readonly IEnumerable<INotificationProvider> _providers;
        private readonly NotificationMessageBuilder _builder;

        public NotificationService(
            IEnumerable<INotificationProvider> providers,
            NotificationMessageBuilder builder) {
            _providers = providers;
            _builder = builder;
        }
        public NotificationService(NotificationMessageBuilder builder) {//temporal constructor
            _builder = builder;

            var httpClient = new HttpClient();

            _providers = new List<INotificationProvider>
            {
                new SlackDmNotificationProvider(
                    httpClient,
                    "xoxb-11332573096805-11337848082193-HcJG03IYWsLh3T9UY1PqFlJP"),

                new TeamsNotificationProvider(
                    httpClient,
                    "https://outlook.office.com/webhook/DEBUG/WEBHOOK")
            };
        }
        public async Task SendErrorReportAsync(ObservableCollection<IssueViewModel> issues) {
            if (issues == null || issues.Count == 0)
                return;

            var errorIssues = issues
                .Where(i => i.Severity == "ERROR")
                .ToList();

            if (!errorIssues.Any())
                return;

            // GROUP BY ARTIST
            var issuesByArtist = errorIssues
                .GroupBy(i => i.Artist?.ArtistName ?? "Unknown")
                .ToDictionary(
                    g => g.Key,
                    g => g.ToList()
                );

            foreach (var provider in _providers) {
                Console.WriteLine($"[Notification] Provider: {provider.Name}");

                foreach (var artistGroup in issuesByArtist) {
                    var artistName = artistGroup.Key;
                    var artistIssues = artistGroup.Value;

                    Console.WriteLine($"[Notification] Sending for artist: {artistName}");

                    var message = _builder.Build(artistIssues);

                    await provider.SendAsync(message);
                }
            }
        }
    }
}