using System.Threading.Tasks;
namespace ValidationTool.Services.Notifications {
    public interface INotificationProvider {
        string Name { get; }
        Task SendAsync(NotificationMessage message);
    }
    public class NotificationMessage {
        public string Title { get; set; } = string.Empty;

        public string Body { get; set; } = string.Empty;

        public string RecipientId { get; set; } = string.Empty;
    }
}