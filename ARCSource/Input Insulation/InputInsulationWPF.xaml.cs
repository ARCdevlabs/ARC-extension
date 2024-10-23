using Autodesk.Revit.DB;
using Autodesk.Revit.UI;
using System;
using System.Collections.ObjectModel;
using System.ComponentModel;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Controls.Primitives;


namespace Input_Insulation
{

    public class ReactiveProperty<T> : INotifyPropertyChanged
    //  Generic Class ReactiveProperty<T>:
    //Đây là một lớp generic(T là một kiểu dữ liệu bất kỳ). Lớp này cho phép tạo các thuộc tính có thể
    //thông báo thay đổi mà không cần viết lại mã cho từng kiểu dữ liệu cụ thể.
    {
        private T _value;
        public T Value
        {
            get => _value;
            set
            {
                if (!Equals(_value, value))
                {
                    _value = value;
                    OnPropertyChanged(nameof(Value));
                }
            }
        }

        public event PropertyChangedEventHandler PropertyChanged;
        protected virtual void OnPropertyChanged(string propertyName)
        {
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
        }
    }

    //  Thuộc tính Value:
    //Đây là thuộc tính chính của lớp, chứa giá trị kiểu T.
    //Getter(get => _value;): Trả về giá trị hiện tại của _value.
    //Setter(set):
    //So sánh giá trị mới(value) với giá trị hiện tại(_value). Nếu khác nhau, giá trị sẽ được cập nhật.
    //Sau khi cập nhật, phương thức OnPropertyChanged sẽ được gọi để thông báo rằng thuộc tính này đã thay đổi.

    //  Phương thức OnPropertyChanged:
    //Phương thức này chịu trách nhiệm thông báo sự thay đổi của thuộc tính.
    //Nó nhận một chuỗi propertyName, là tên của thuộc tính thay đổi.
    //PropertyChanged là sự kiện thuộc kiểu PropertyChangedEventHandler.
    //Khi sự kiện này được kích hoạt, nó sẽ thông báo cho tất cả các thành phần lắng nghe rằng thuộc tính đã thay đổi.

    public class ButtonDataCuaSon : INotifyPropertyChanged
    {
        private string _title;
        public string binding_title_new_button
        {
            get => _title;
            set
            {
                if (_title != value)
                {
                    _title = value;
                    OnPropertyChanged(nameof(binding_title_new_button));
                }
            }
        }
        //    Interface INotifyPropertyChanged:
        //Lớp ReactiveProperty<T> triển khai interface INotifyPropertyChanged.
        //Interface này yêu cầu phải có sự kiện PropertyChanged, được sử dụng để
        //thông báo cho giao diện người dùng hoặc các thành phần khác rằng thuộc tính đã thay đổi.
        //Đây là cơ chế cốt lõi trong WPF và các framework MVVM để đảm bảo rằng giao diện
        //người dùng luôn được cập nhật khi dữ liệu thay đổi.


        //      ReactiveProperty<T> cho phép các thuộc tính có khả năng "phản ứng" khi chúng thay đổi.
        //Điều này rất hữu ích khi bạn cần đảm bảo rằng giao diện người dùng hoặc các thành
        //phần khác sẽ được cập nhật ngay lập tức khi dữ liệu thay đổi.

        public ButtonDataCuaSon(string title)
        {
            _title = title;
        }

        public event PropertyChangedEventHandler PropertyChanged;
        protected virtual void OnPropertyChanged(string propertyName)
        {
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
        }
    }

    public class ListViewItem : INotifyPropertyChanged
    {
        private int _value;
        private bool _isChecked;

        public int Value => _value;
        public bool IsChecked
        {
            get => _isChecked;
            set
            {
                if (_isChecked != value)
                {
                    _isChecked = value;
                    OnPropertyChanged(nameof(IsChecked));
                }
            }
        }

        public ListViewItem(int value)
        {
            _value = value;
            _isChecked = false;
        }

        public event PropertyChangedEventHandler PropertyChanged;
        protected virtual void OnPropertyChanged(string propertyName)
        {
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
        }
    }

    public partial class MainWindow : Window
    {
        private ObservableCollection<ListViewItem> _listTest;
        private bool _inCheck = false;
        private bool _inUncheck = false;

        public MainWindow()
        {
            InitializeComponent();
            Setup();
        }

        private void Setup()
        {
            _listTest = new ObservableCollection<ListViewItem>();
            for (int i = 1; i <= 50; i++)
            {
                _listTest.Add(new ListViewItem(i));
            }

            new_button.DataContext = new ButtonDataCuaSon("Đây là button của Sơn");
            search_tb.TextChanged += SearchTb_TextChanged;
            list_lb.ItemsSource = _listTest;
        }

        private void SearchTb_TextChanged(object sender, TextChangedEventArgs e)
        {
            string searchText = search_tb.Text.ToLower();
            var filteredList = new ObservableCollection<ListViewItem>();
            foreach (var item in _listTest)
            {
                if (item.Value.ToString().Contains(searchText))
                {
                    filteredList.Add(item);
                }
            }
            list_lb.ItemsSource = filteredList;
        }

        private void click_button_cua_son(object sender, RoutedEventArgs e)
        {
            // Tạo TaskDialog
            TaskDialog td = new TaskDialog("Giá trị đã nhập");
            td.TitleAutoPrefix = false;
            td.MainInstruction = search_tb.Text.ToString();
            td.FooterText = "Nguyễn Thanh Sơn";
            td.CommonButtons = TaskDialogCommonButtons.Ok | TaskDialogCommonButtons.Cancel;
            td.VerificationText = "Test Verify";
            // Hiển thị TaskDialog
            td.Show();

        }

        private void hanh_dong_button_print(object sender, RoutedEventArgs e)
        {
            var checkedValues = new System.Text.StringBuilder();
            foreach (var item in list_lb.ItemsSource)
            {
                if (((ListViewItem)item).IsChecked)
                {
                    checkedValues.Append(((ListViewItem)item).Value.ToString() + ", ");
                }
            }

            TaskDialog.Show("Ô đã check", checkedValues.ToString().TrimEnd(',', ' '));
            Hide();
            Show();
        }

        private void check_box_Checked(object sender, RoutedEventArgs e)
        {
            if (!_inCheck)
            {
                try
                {
                    foreach (ListViewItem item in list_lb.SelectedItems)
                    {
                        item.IsChecked = true;
                    }
                }
                finally
                {
                    _inCheck = false;
                }
            }
        }

        private void check_box_Unchecked(object sender, RoutedEventArgs e)
        {
            if (!_inUncheck)
            {
                try
                {
                    foreach (ListViewItem item in list_lb.SelectedItems)
                    {
                        item.IsChecked = false;
                    }
                }
                finally
                {
                    _inUncheck = false;
                }
            }
        }

    }

}
