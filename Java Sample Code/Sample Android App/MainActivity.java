package edu.gatech.seclass.sdpencryptor;

import android.content.Context;

import androidx.appcompat.app.AppCompatActivity;
import android.view.View;
import android.os.Bundle;
import android.widget.EditText;
import android.widget.RadioButton;
import android.view.inputmethod.InputMethodManager;

public class MainActivity extends AppCompatActivity {
    private RadioButton radioButtonEncrypt;
    private EditText Entry_Text;
    private EditText Input1;
    private EditText Input2;
    private EditText Result;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        // from an id to an actual objects, recovery the class using this mapping method
        Entry_Text = (EditText) findViewById(R.id.entryTextID);
        Input1 = (EditText) findViewById(R.id.argInput1ID);
        Input2 = (EditText) findViewById(R.id.argInput2ID);

        Result = (EditText) findViewById(R.id.textEncryptedID);
        Result.setEnabled(false);

        // final TextView Result = (TextView) findViewById(R.id.textEncryptedID);

    }

    public void handleClick(View view) {
        // Close the keyboard
        InputMethodManager inputManager = (InputMethodManager) getSystemService(Context.INPUT_METHOD_SERVICE);
        View currentFocusedView = this.getCurrentFocus();
        if (currentFocusedView != null) {
            inputManager.hideSoftInputFromWindow(currentFocusedView.getWindowToken(), InputMethodManager.HIDE_NOT_ALWAYS);
        }

        if (view.getId() == R.id.encryptButtonID) {
            // Initialize a boolean to track if there are any errors
            boolean hasError = false;

            String result;
            String Input_Text = Entry_Text.getText().toString();
            int input1Int = Integer.parseInt(Input1.getText().toString());
            int input2Int = Integer.parseInt(Input2.getText().toString());
            try {
                if (Input_Text == null || LetterOStr(Input_Text) == false) {
                    Entry_Text.setError("Invalid Entry Text");
                    Result.setText("");
                    hasError = true;
                }
            } catch (NumberFormatException e) {
                Entry_Text.setError("Invalid Entry Text");
                Result.setText("");
            }

            try {
                if (CoPrime(input1Int, 62) != 1 || !(1 <= input1Int && input1Int < 62)) {
                    Input1.setError("Invalid Arg Input 1");
                    Result.setText("");
                    hasError = true;

                }
            } catch (NumberFormatException e) {
                Input1.setError("Invalid Arg Input 1");
                Result.setText("");
            }

            try {
                if (!(1 <= input2Int && input2Int < 62)) {

                    Input2.setError("Invalid Arg Input 2");
                    Result.setText("");
                    hasError = true;

                }
            } catch (NumberFormatException e) {
                Input2.setError("Invalid Arg Input 2");
                Result.setText("");
            }

            if (hasError == false) {
                result = Encryptor(Input_Text, input1Int, input2Int);
                Result.setText(result);
            }


        }
    }

    private String Encryptor(String Entry_Text, int Input1, int Input2) {

        StringBuilder encrypt_res = new StringBuilder();
        for (char C : Entry_Text.toCharArray()) {
            if (Character.isLetterOrDigit(C)) {
                // covert to number
                int num_C = (CharTNum(C) * Input1 + Input2) % 62;

                // covert to string
                char res = NumTChar(num_C);
                encrypt_res.append(res);
            } else {
                // All non-alphanumeric characters must remain unchanged.
                encrypt_res.append(C);
            }

        }
        return encrypt_res.toString();

    }

    // converge from char to number
    public int CharTNum(char C) {
        int res = 0;
        if (Character.isDigit(C)) {
            // '0' to '9' => 0 to 9
            res = C - '0';
            return res;
        } else if (Character.isUpperCase(C)) {
            // 'A' to 'Z' => 10 to 35
            res = C - 'A' + 10;
            return res;
        } else {
            // 'a' to 'z' => 36 to 61
            res = C - 'a' + 36;
            return res; // 'a' to 'z' => 36 to 61
        }

    }

    // converge from number to char
    public char NumTChar(int num) {
        if (num <= 9) {
            // '0' to '9' => 0 to 9
            return (char) ('0' + num);
        }
        // 'A' to 'Z' => 10 to 35
        else if (num <= 35) {
            return (char) ('A' + num - 10);
        }
        // 'a' to 'z' => 36 to 61
        else if (num <= 61) {
            return (char) ('a' + num - 36);
        }
        throw new IllegalArgumentException("Number is out of valid range for character conversion");

    }

//  arg1 should be an integer co-prime to 62 between 0 and 62

    public int CoPrime(int num1, int num2) {
        while (num2 != 0) {
            int temp = num2;
            num2 = num1 % num2;
            num1 = temp;
        }
        return num1;

    }


    //string does not contain at least one letter or number
    public boolean LetterOStr(String string) {
        for (char c : string.toCharArray()) {
            if (Character.isLetterOrDigit(c)) {
                return true;
            }
        }
        return false;
    }
}



