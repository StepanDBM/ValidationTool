using System;
using System.Windows.Input;

namespace ValidationTool.UI.Commands {
    public class RelayCommand<T> : ICommand {
        private readonly Action<T> _execute;
        private readonly Func<T, bool> _canExecute;

        public RelayCommand(Action<T> execute, Func<T, bool> canExecute = null) {
            _execute = execute ?? throw new ArgumentNullException(nameof(execute));
            _canExecute = canExecute;
        }

        public event EventHandler CanExecuteChanged;

        public bool CanExecute(object parameter) {
            if (_canExecute == null)
                return true;

            if (parameter == null) {
                if (default(T) == null)
                    return _canExecute(default(T));

                return false;
            }

            if (parameter is T validParameter)
                return _canExecute(validParameter);

            return false;
        }

        public void Execute(object parameter) {
            if (parameter == null) {
                if (default(T) == null) {
                    _execute(default(T));
                    return;
                }

                throw new ArgumentNullException(nameof(parameter));
            }

            if (parameter is T validParameter) {
                _execute(validParameter);
                return;
            }

            throw new InvalidCastException(
                $"Command parameter is of type '{parameter.GetType().FullName}' but expected '{typeof(T).FullName}'.");
        }

        public void RaiseCanExecuteChanged() {
            CanExecuteChanged?.Invoke(this, EventArgs.Empty);
        }
    }
}
