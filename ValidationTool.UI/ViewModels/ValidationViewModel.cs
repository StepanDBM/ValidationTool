using System;
using System.Collections.ObjectModel;
using System.ComponentModel;
using System.IO;
using System.Linq;
using System.Windows;
using System.Windows.Data;
using ValidationTool.UI.Models.DTOs;
using ValidationTool.UI.Services;
using ValidationTool.UI.Services.Config;
using ValidationTool.UI.Services.external;

namespace ValidationTool.UI.ViewModels {
    public class ValidationViewModel : INotifyPropertyChanged{

        public ObservableCollection<IssueViewModel> mIssues { get; set; } = new ObservableCollection<IssueViewModel>();
        public ObservableCollection<ValidationRunDto> mRun { get; set; } = new ObservableCollection<ValidationRunDto>();


        public ICollectionView IssuesView { get; set; }

        public ValidationViewModel() {

            IssuesView = CollectionViewSource.GetDefaultView(mIssues);
        }


        public event PropertyChangedEventHandler PropertyChanged;
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
        private int _totalInfos;
        public int TotalInfos {
            get => _totalInfos;
            set {
                _totalInfos = value;
                PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(nameof(TotalInfos)));
            }
        }

        public void LoadReport() {
            TotalAssets = 0;
            TotalIssues = 0;
            TotalErrors = 0;
            TotalWarnings = 0;
            TotalInfos = 0;
            mIssues.Clear();
            var dtos = JsonReportLoader.Load();

            foreach (var dcc in dtos) {
                TotalAssets += dcc.summary.TotalAssets;
                TotalIssues += dcc.summary.TotalIssues;
                TotalErrors += dcc.summary.Errors;
                TotalWarnings += dcc.summary.Warnings;
                TotalInfos += dcc.summary.Infos;
                foreach (var issue in dcc.issues) {
                    mIssues.Add(new IssueViewModel {
                        Artist = new ArtistViewModel {
                            ArtistName = issue.Artist.ArtistName,
                            ArtistLevel = issue.Artist.ArtistLevel,
                            ArtistID = issue.Artist.ArtistID
                        },
                        Dcc = issue.Dcc,
                        Timestamp = issue.Timestamp.ToString(),
                        Asset_name = issue.AssetName,
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
                    Infos = TotalInfos,
                }
            });
            dtos.Clear();
        }
        private Func<IssueViewModel, object> getKeySelector(string header) {
            Func<IssueViewModel, object> keySelector = null;
            switch (header) {
                case "Artist":
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

        public void RunMayaValidation() {
            MayaRunner.Run(Path.Combine(Paths.HEADLESS, "run_maya_validation.py"),
                line =>
            {
                Application.Current.Dispatcher.Invoke(() =>
                {
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
                });
            });
        }
        public void RunBlenderValidation() {
            BlenderRunner.Run(Path.Combine(Paths.HEADLESS, "run_blender_validation.py"),
                line =>
                {
                    Application.Current.Dispatcher.Invoke(() =>
                    {
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
                    });
                });
        }
    }
}