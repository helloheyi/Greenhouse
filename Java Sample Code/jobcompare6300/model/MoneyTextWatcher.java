package edu.gatech.seclass.jobcompare6300.model;

import android.text.Editable;
import android.text.TextWatcher;
import android.widget.EditText;


public class MoneyTextWatcher implements TextWatcher {
    private EditText editText;

    public MoneyTextWatcher(EditText editText) {
        this.editText = editText;
    }

    @Override
    public void beforeTextChanged(CharSequence s, int start, int count, int after) {

    }

    /* BEGIN CODE FROM https://drprincess.github.io/2017/10/09/Android-EditText%E9%99%90%E5%88%B6%E8%BE%93%E5%85%A5%E4%B8%A4%E4%BD%8D%E5%B0%8F%E6%95%B0/*/
    @Override
    public void onTextChanged(CharSequence s, int start, int before, int count) {
        // Delete the number after .xx
        if (s.toString().contains(".")) {
            if (s.length() - 1 - s.toString().indexOf(".") > 2) {
                s = s.toString().subSequence(0,
                        s.toString().indexOf(".") + 2+1);
                editText.setText(s);
                editText.setSelection(s.length()); //mouse move to the end
            }
        }

        // If "." is at the beginning, add a "0" before the "."
        if (s.toString().trim().substring(0).equals(".")) {
            s = "0" + s;
            editText.setText(s);
            editText.setSelection(2);
        }

        // If the first number is 0, and the second is not ".", it is not allowed to input
        if (s.toString().startsWith("0") && s.toString().trim().length() > 1) {
            if (!s.toString().substring(1, 2).equals(".")) {
                editText.setText(s.subSequence(0, 1));
                editText.setSelection(1);
            }
        }
    }
    /* END CODE FROM https://drprincess.github.io/2017/10/09/Android-EditText%E9%99%90%E5%88%B6%E8%BE%93%E5%85%A5%E4%B8%A4%E4%BD%8D%E5%B0%8F%E6%95%B0/*/

    @Override
    public void afterTextChanged(Editable s) {

    }
}
