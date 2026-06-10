using System.Collections.ObjectModel;
using ValidationTool.UI.Services;
using ValidationTool.UI.Services.Config;
using ValidationTool.UI.Services.external;
using System.IO;
using ValidationTool.UI.Models.DTOs;
using System.ComponentModel;

namespace ValidationTool.UI.ViewModels {
    public class ValidationViewModel : INotifyPropertyChanged{

        public ObservableCollection<IssueViewModel> mIssues { get; set; }
            = new ObservableCollection<IssueViewModel>();
        public ObservableCollection<ValidationRunDto> mRun { get; set; } = new ObservableCollection<ValidationRunDto>();

        public event PropertyChangedEventHandler PropertyChanged;
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
            var dtos = JsonReportLoader.Load();

            foreach (var dcc in dtos) {
                TotalAssets += dcc.summary.TotalAssets;
                TotalIssues += dcc.summary.TotalIssues;
                TotalErrors += dcc.summary.Errors;
                TotalWarnings += dcc.summary.Warnings;
                TotalInfos += dcc.summary.Infos;
                foreach (var issue in dcc.issues) {
                    mIssues.Add(new IssueViewModel {
                        Artist = issue.Artist.ArtistName,
                        A_lv = issue.Artist.ArtistLevel,
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

        public void RunMayaValidation() {
            MayaRunner.Run(Path.Combine(Paths.HEADLESS, "run_maya_validation.py"));
        }
        public void RunBlenderValidation() {
            BlenderRunner.Run(Path.Combine(Paths.HEADLESS, "run_blender_validation.py"));
        }
    }
}