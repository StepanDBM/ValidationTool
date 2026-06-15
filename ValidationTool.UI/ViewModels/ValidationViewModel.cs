using System;
using System.Collections.ObjectModel;
using System.ComponentModel;
using System.Diagnostics;
using System.Globalization;
using System.IO;
using System.Linq;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Data;
using ValidationTool.Services.Notifications;
using ValidationTool.UI.Models.DTOs;
using ValidationTool.UI.Services;
using ValidationTool.UI.Services.Config;
using ValidationTool.UI.Services.external;
using ValidationTool.UI.Services.External;
using ValidationTool.UI.Services.Notifications;

namespace ValidationTool.UI.ViewModels {
    public class ValidationViewModel : INotifyPropertyChanged {
        public SelectionContext Selection { get; } = new SelectionContext();
        public UC_TeamListViewModel TeamListVM { get; }
        public UC_ArtistListViewModel ArtistListVM { get; }
        public UC_FileListViewModel FileListVM { get; }
        public ObservableCollection<IssueViewModel> mIssues { get; set; } = new ObservableCollection<IssueViewModel>();
        public ObservableCollection<ValidationRunDto> mRun { get; set; } = new ObservableCollection<ValidationRunDto>();

        //private NotificationService mNotService = new NotificationService(new NotificationMessageBuilder());
        public ICollectionView IssuesView { get; set; }

        public ValidationViewModel() {

            IssuesView = CollectionViewSource.GetDefaultView(mIssues);
            TeamListVM = new UC_TeamListViewModel(mIssues, Selection);
            ArtistListVM = new UC_ArtistListViewModel(mIssues, Selection);
            FileListVM = new UC_FileListViewModel(mIssues, Selection);

            Selection.PropertyChanged += OnSelectionChanged;
        }


        public event PropertyChangedEventHandler PropertyChanged;

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


        private string _myNewText;
        public string myNewText {
            get => _myNewText;
            set {
                _myNewText = value;
                PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(nameof(myNewText)));
            }
        }

        public void LoadReport() {
            myNewText = "SHIEHHHHHH";
            TotalAssets = 0;
            TotalIssues = 0;
            TotalErrors = 0;
            TotalWarnings = 0;
            TotalScenes = 0;
            mIssues.Clear();
            var dtos = JsonReportLoader.Load();

            foreach (var scene in dtos) {
                TotalAssets += scene.summary.TotalAssets;
                TotalIssues += scene.summary.TotalIssues;
                TotalErrors += scene.summary.Errors;
                TotalWarnings += scene.summary.Warnings;
                TotalScenes += 1;
                foreach (var issue in scene.issues) {
                    mIssues.Add(new IssueViewModel {
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
                        Timestamp = issue.Timestamp.ToString(),
                        Asset_name = issue.ObjectName,
                        Check_name = issue.CheckName,
                        Severity = issue.Severity,
                        Message = issue.Message,
                        Suggestion = issue.Suggestion,
                        Stage = issue.Stage
                    });
                }
            }
            mRun.Add(new ValidationRunDto {
                summary = new RunSummaryDto {
                    RunId = "",
                    Timestamp = System.DateTime.Now,
                    Dcc = "",
                    TotalAssets = TotalAssets,
                    TotalIssues = TotalIssues,
                    Errors = TotalErrors,
                    Warnings = TotalWarnings,
                    Infos = TotalScenes,
                }
            });
            TeamListVM.AggregateAll();
            //mNotService.SendErrorReportAsync(mIssues);
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

        public class InverseBoolConverter : IValueConverter {
            public object Convert(object value, Type targetType, object parameter, CultureInfo culture) {
                return !(bool)value;
            }

            public object ConvertBack(object value, Type targetType, object parameter, CultureInfo culture) {
                return !(bool)value;
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
    }
}