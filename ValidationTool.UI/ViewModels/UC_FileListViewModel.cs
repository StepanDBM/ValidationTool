using System;
using System.Collections.ObjectModel;
using System.ComponentModel;
using System.IO;
using System.Linq;
using System.Text.Json;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Input;
using ValidationTool.Services.Notifications;
using ValidationTool.UI.Commands;
using ValidationTool.UI.Models.DTOs;
using ValidationTool.UI.Services.Config;
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

        private readonly ObservableCollection<ValidationRunDto> _runs;

        public UC_FileListViewModel(
            ObservableCollection<IssueViewModel> issues,
            ObservableCollection<ValidationRunDto> runs,
            SelectionContext selection) {

            SendReportCommand = new AsyncRelayCommand<FileStatsViewModel>(SendReport);
            _issues = issues;
            _runs = runs;
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

            var filteredRuns = _runs
                .Where(r =>
                    r.issues != null &&
                    r.issues.Any(i =>
                        i.Artist?.ArtistTeam == _selection.SelectedTeam &&
                        i.Artist?.ArtistName == _selection.SelectedArtist));

            foreach (var run in filteredRuns) {
                if (run.issues == null || run.issues.Count == 0)
                    continue;

                var firstIssue = run.issues.FirstOrDefault();
                if (firstIssue == null)
                    continue;

                int errors = run.issues.Count(i => i.Severity == "ERROR");
                int warnings = run.issues.Count(i => i.Severity == "WARNING");
                int infos = run.issues.Count(i => i.Severity == "INFO");

                string filePath = firstIssue.OriginFile;
                string fileName = Path.GetFileName(filePath);

                FileList.Add(new FileStatsViewModel {
                    FileName = fileName,
                    FilePath = filePath,
                    Errors = errors,
                    Warnings = warnings,
                    Issues = errors + warnings + infos,
                    SceneSetup = run.scene_setup
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
            if (file == null) {
                MessageBox.Show(
                    "No file was passed to the Scene Setup view.",
                    "Scene Setup",
                    MessageBoxButton.OK,
                    MessageBoxImage.Warning);
                return;
            }

            if (file.SceneSetup == null) {
                MessageBox.Show(
                    "No Scene Setup data found for the selected file.",
                    "Scene Setup",
                    MessageBoxButton.OK,
                    MessageBoxImage.Warning);
                return;
            }

            var wnd = new SceneSetupWndw(file.SceneSetup);
            wnd.Show();
        }
    }
}