using System;
using System.Collections.ObjectModel;
using System.ComponentModel;
using System.IO;
using System.Linq;
using System.Threading.Tasks;
using System.Windows.Input;
using ValidationTool.Services.Notifications;
using ValidationTool.UI.Commands;
using ValidationTool.UI.Models.DTOs;
using ValidationTool.UI.ViewModels.ValidationView_Models;
using ValidationTool.UI.Views;

namespace ValidationTool.UI.ViewModels {
    public class UC_FileListViewModel {
        private readonly ObservableCollection<IssueViewModel> _issues;
        private readonly SelectionContext _selection;

        private NotificationService mNotService = new NotificationService(new NotificationMessageBuilder());
        public ICommand SendReportCommand { get; }

        public ObservableCollection<FileStatsViewModel> FileList { get; } =new ObservableCollection<FileStatsViewModel>();

        public ICommand OpenSceneConfigViewCommand { get; }

        public UC_FileListViewModel( ObservableCollection<IssueViewModel> issues, SelectionContext selection) {
            SendReportCommand = new AsyncRelayCommand<FileStatsViewModel>(SendReport);
            _issues = issues;
            _selection = selection;

            _selection.PropertyChanged += OnSelectionChanged;
            OpenSceneConfigViewCommand = new RelayCommand<FileStatsViewModel>(OpenSceneConfigView);
        }
        private FileStatsViewModel _selectedFileVM;
        public FileStatsViewModel SelectedFileVM {
            get => _selectedFileVM;
            set {
                _selectedFileVM = value;

                if (value != null) {
                    _selection.SelectedFile = value.FilePath;
                }
            }
        }

        private void OnSelectionChanged(object sender, PropertyChangedEventArgs e) {
            if (e.PropertyName == nameof(_selection.SelectedArtist) ||
                e.PropertyName == nameof(_selection.SelectedTeam)) {
                FilterFiles();
            }
        }

        private void FilterFiles() {
            FileList.Clear();

            if (string.IsNullOrEmpty(_selection.SelectedTeam) ||
                string.IsNullOrEmpty(_selection.SelectedArtist))
                return;

            var filtered = _issues
                .Where(i =>
                    i.Artist?.ArtistTeam == _selection.SelectedTeam &&
                    i.Artist?.ArtistName == _selection.SelectedArtist)
                .GroupBy(i => i.OriginFile);

            foreach (var g in filtered) {
                int errors = g.Count(i => i.Severity == "ERROR");
                int warnings = g.Count(i => i.Severity == "WARNING");
                int infos = g.Count(i => i.Severity == "INFO");
                string thisName = Path.GetFileName(g.Key);

                //string extension = Path.GetExtension(g.Key);
                FileList.Add(new FileStatsViewModel {
                    FileName = thisName,
                    FilePath = g.Key,
                    Errors = errors,
                    Warnings = warnings,
                    Issues = errors + warnings + infos
                });
            }
        }

        private async Task SendReport(FileStatsViewModel file) {
            try {
                if (file == null) return;

                var fileIssues = new ObservableCollection<IssueViewModel>(
                    _issues.Where(i => i.OriginFile == file.FilePath)
                );

                await mNotService.SendErrorReportAsync(fileIssues);
            } catch (Exception ex) {
                System.Diagnostics.Debug.WriteLine($"[ERROR] {ex.Message}");
            }
        }

        private void OpenSceneConfigView(FileStatsViewModel file) {
            if (file == null)
                return;

            //SceneSetupDto sceneSetup = LoadSceneSetupForFile(file.FilePath);

            //var wnd = new SceneSetupWndw(sceneSetup);
            var wnd = new SceneSetupWndw();
            wnd.Show();
        }


    }
}