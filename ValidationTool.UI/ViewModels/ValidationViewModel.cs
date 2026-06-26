using System;
using System.Collections.ObjectModel;
using System.ComponentModel;
using System.IO;
using System.Linq;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Data;
using System.Windows.Input;
using ValidationTool.Services.Notifications;
using ValidationTool.UI.Services;
using ValidationTool.UI.Models.DTOs.Profiles;
using ValidationTool.UI.Models.DTOs;
using ValidationTool.UI.Services.Config;
using ValidationTool.UI.Services.External;

namespace ValidationTool.UI.ViewModels {
    public class ValidationViewModel : INotifyPropertyChanged {
        public SelectionContext Selection { get; } = new SelectionContext();
        public UC_TeamListViewModel TeamListVM { get; }
        public UC_ArtistListViewModel ArtistListVM { get; }
        public UC_FileListViewModel FileListVM { get; }
        public ObservableCollection<IssueViewModel> mIssues { get; set; } = new ObservableCollection<IssueViewModel>();
        public ObservableCollection<ValidationRunDto> mRun { get; set; } = new ObservableCollection<ValidationRunDto>();


        private NotificationService mNotService = new NotificationService(new NotificationMessageBuilder());
        public ICommand SendReportCommand { get; }
        public ICommand FixIssueCommand { get; }

        public ICollectionView IssuesView { get; set; }

        public ValidationViewModel() {

            IssuesView = CollectionViewSource.GetDefaultView(mIssues);
            TeamListVM = new UC_TeamListViewModel(mIssues, Selection);
            ArtistListVM = new UC_ArtistListViewModel(mIssues, Selection);
            FileListVM = new UC_FileListViewModel(mIssues, mRun, Selection);

            Selection.PropertyChanged += OnSelectionChanged;


            SendReportCommand = new AsyncRelayCommand<IssueViewModel>(SendReport);
            FixIssueCommand = new AsyncRelayCommand<IssueViewModel>(FixIssue);

            LoadProfilesForDropdown();
        }


        public event PropertyChangedEventHandler PropertyChanged;
        public ObservableCollection<string> LogLines { get; } = new ObservableCollection<string>();

        private bool _isBusy;
        public bool IsBusy {
            get => _isBusy;
            set {
                _isBusy = value;
                PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(nameof(IsBusy)));
            }
        }

        private string _currentFile;
        public string CurrentFile {
            get => _currentFile;
            set {
                _currentFile = value;
                PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(nameof(CurrentFile)));
            }
        }
        private int _progress;
        public int Progress {
            get => _progress;
            set {
                _progress = value;
                PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(nameof(Progress)));
            }
        }

        private int _totalAssets;
        public int TotalAssets {
            get => _totalAssets;
            set {
                _totalAssets = value;
                PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(nameof(TotalAssets)));
            }
        }

        private int _totalIssues;
        public int TotalIssues {
            get => _totalIssues;
            set {
                _totalIssues = value;
                PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(nameof(TotalIssues)));
            }
        }

        private int _totalErrors;
        public int TotalErrors {
            get => _totalErrors;
            set {
                _totalErrors = value;
                PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(nameof(TotalErrors)));
            }
        }

        private int _totalWarnings;
        public int TotalWarnings {
            get => _totalWarnings;
            set {
                _totalWarnings = value;
                PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(nameof(TotalWarnings)));
            }
        }
        private int _totalScenes;
        public int TotalScenes {
            get => _totalScenes;
            set {
                _totalScenes = value;
                PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(nameof(TotalScenes)));
            }
        }


        private readonly ProfilesConfigService _profilesConfigService = new ProfilesConfigService();

        private readonly ActiveProfileService _activeProfileService = new ActiveProfileService();

        public ObservableCollection<ProfileDto> AvailableProfiles { get; } =
            new ObservableCollection<ProfileDto>();

        private ProfileDto _selectedProfile;
        public ProfileDto SelectedProfile {
            get => _selectedProfile;
            set {
                _selectedProfile = value;
                PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(nameof(SelectedProfile)));
                WriteActiveProfile();
            }
        }


        public void LoadReport() {
            TotalAssets = 0;
            TotalIssues = 0;
            TotalErrors = 0;
            TotalWarnings = 0;
            TotalScenes = 0;
            mIssues.Clear();
            var dtos = JsonReportLoader.Load();
            Progress = 0;
            int length = 0;
            int current = 0;
            foreach (var scene in dtos) {
                length++;
            }
            foreach (var scene in dtos) {
                mRun.Add(scene);
                TotalAssets += scene.summary.TotalAssets;
                TotalIssues += scene.summary.TotalIssues;
                TotalErrors += scene.summary.Errors;
                TotalWarnings += scene.summary.Warnings;
                TotalScenes += 1;
                foreach (var issue in scene.issues) {
                    var someIssue = new IssueViewModel {
                        Artist = new ArtistViewModel {
                            ArtistName = issue.Artist.ArtistName,
                            ArtistLevel = issue.Artist.ArtistLevel,
                            ArtistID = issue.Artist.ArtistID,
                            LeadArtist = issue.Artist.LeadArtist,
                            ArtistTeam = issue.Artist.ArtistTeam,
                            ArtistSlackID = issue.Artist.ArtistSlackID,
                            ArtistTeamsID = issue.Artist.ArtistTeamsID,
                            ArtistGmail = issue.Artist.ArtistGmail
                        },
                        Dcc = issue.Dcc,
                        OriginFile = issue.OriginFile,
                        Asset_name = issue.ObjectName,
                        Check_name = issue.CheckName,
                        Stage = issue.Stage,
                        Timestamp = issue.Timestamp.ToString(),
                        Severity = issue.Severity,
                        Message = issue.Message,
                        Suggestion = issue.Suggestion,
                        FixModeRaw = issue.FixMode
                    };
                    mIssues.Add(someIssue);
                }
                current++;
                Progress = (int)((double)current / length * 100);
                string line = "Loaded: " + scene.scene_setup.SceneName + " TOTAL PROGRESS: [" + Progress + "%]";
                ProcessLine(line);
            }
            TeamListVM.AggregateAll();

            dtos.Clear();
        }
        private Func<IssueViewModel, object> getKeySelector(string header) {
            Func<IssueViewModel, object> keySelector = null;
            switch (header) {
                case "Artist.Team":
                    keySelector = x => x.Artist?.ArtistTeam ?? "";
                    break;
                case "Artist.LeadArtist":
                    keySelector = x => x.Artist?.LeadArtist ?? "";
                    break;
                case "Artist.ArtistName":
                    keySelector = x => x.Artist?.ArtistName ?? "";
                    break;

                case "Level":
                case "Artist.ArtistLevel":
                    keySelector = x => x.Artist?.ArtistLevel ?? "";
                    break;

                case "Severity":
                    keySelector = x => x.Severity ?? "";
                    break;

                case "Asset":
                case "Asset_name":
                    keySelector = x => x.Asset_name ?? "";
                    break;

                case "Stage":
                    keySelector = x => x.Stage ?? "";
                    break;

                case "Message":
                    keySelector = x => x.Message ?? "";
                    break;

                case "Suggestion":
                    keySelector = x => x.Suggestion?? "";
                    break;

                default:
                    keySelector = x => x.Asset_name ?? "";
                    break;
            }
            return keySelector;
        }
        public void GridViewColumnHeader_Click(string header, bool ascending) {
            Func<IssueViewModel, object> keySelector = null;

            keySelector = getKeySelector(header);

            var sorted = ascending
                ? mIssues.OrderBy(keySelector).ToList()
                : mIssues.OrderByDescending(keySelector).ToList();

            mIssues.Clear();

            foreach (var item in sorted)
                mIssues.Add(item);

            IssuesView.Refresh();
        }

        private void OnSelectionChanged(object sender, PropertyChangedEventArgs e) {
            if (e.PropertyName == nameof(Selection.SelectedTeam) ||
                e.PropertyName == nameof(Selection.SelectedArtist) ||
                e.PropertyName == nameof(Selection.SelectedFile)) {
                ApplyIssueFilter();
            }
        }

        private void ApplyIssueFilter() {
            IssuesView.Filter = obj =>
            {
                var issue = obj as IssueViewModel;
                if (issue == null) return false;

                if (!string.IsNullOrEmpty(Selection.SelectedTeam) &&
                    issue.Artist?.ArtistTeam != Selection.SelectedTeam)
                    return false;

                if (!string.IsNullOrEmpty(Selection.SelectedArtist) &&
                    issue.Artist?.ArtistName != Selection.SelectedArtist)
                    return false;

                if (!string.IsNullOrEmpty(Selection.SelectedFile) &&
                    issue.OriginFile != Selection.SelectedFile)
                    return false;

                return true;
            };

            IssuesView.Refresh();
        }
        private void ProcessLine(string line) {
            Application.Current.Dispatcher.Invoke(() => {
                LogLines.Add(line);
                if (LogLines.Count > 500)
                    LogLines.RemoveAt(0);
            });

            if (line.StartsWith("PROGRESS:")) {
                var percentText = line
                    .Replace("PROGRESS:", "")
                    .Replace("[", "")
                    .Replace("%]", "")
                    .Trim();

                if (int.TryParse(percentText, out int value)) {
                    Progress = value;
                }
            }

            if (line.StartsWith("CURRENT_FILE:")) {
                CurrentFile = line.Replace("CURRENT_FILE:", "").Trim();
            }
        }

        public async Task RunMayaValidation() {
            IsBusy = true;

            try {
                await Task.Run(() =>
                {
                    MayaRunner.Run(
                        Path.Combine(Paths.HEADLESS, "run_maya_validation.py"),
                        line => {
                            Application.Current.Dispatcher.Invoke(() => {
                                ProcessLine(line);
                            });
                        });
                });
            } finally {
                IsBusy = false;
                LoadReport();
            }
        }

        public async Task RunBlenderValidation() {
            IsBusy = true;
            try {
                await Task.Run(() => {
                    BlenderRunner.Run(
                        Path.Combine(Paths.HEADLESS, "run_blender_validation.py"),
                        line => {
                            Application.Current.Dispatcher.Invoke(() => {
                                ProcessLine(line);
                            });
                        });
                });
            } finally {
                IsBusy = false;
                LoadReport();
            }
        }
        public async Task LoadProxy() {
            IsBusy = true;

            try {
                await Task.Run(() =>
                {
                    ArtistsDataSetCreator.Run(line =>
                    {
                        Application.Current.Dispatcher.Invoke(() =>
                        {
                            ProcessLine(line);
                        });
                    });
                });
            } finally {
                IsBusy = false;
            }
        }

        private async Task SendReport(IssueViewModel issue) {
            try {
                if (issue == null) return;
                ObservableCollection<IssueViewModel> issueList = new ObservableCollection<IssueViewModel>() { issue};
                await mNotService.SendErrorReportAsync(issueList, true);
            } catch (Exception ex) {
                System.Diagnostics.Debug.WriteLine($"[ERROR] {ex.Message}");
            }
        }

        private async Task FixIssue(IssueViewModel issue) {
            Console.WriteLine($"The issue is: {issue.Check_name}, {issue.Message}, {issue.Suggestion}");
        }


        private void LoadProfilesForDropdown() {
            AvailableProfiles.Clear();

            var profilesFile = _profilesConfigService.Load();

            foreach (var profile in profilesFile.profiles) {
                AvailableProfiles.Add(profile);
            }

            SelectedProfile = AvailableProfiles.FirstOrDefault();
        }

        private void WriteActiveProfile() {
            try {
                _activeProfileService.Save(SelectedProfile);

                if (SelectedProfile != null) {
                    ProcessLine($"ACTIVE_PROFILE: {SelectedProfile.name}");
                }
            } catch (Exception ex) {
                ProcessLine($"[ERR] Could not write active profile: {ex.Message}");
            }
        }
    }
}