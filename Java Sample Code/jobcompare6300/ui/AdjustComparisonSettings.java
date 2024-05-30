package edu.gatech.seclass.jobcompare6300.ui;

import androidx.appcompat.app.AppCompatActivity;
import edu.gatech.seclass.jobcompare6300.R;

import androidx.appcompat.app.AppCompatActivity;
import android.content.Intent;
import android.app.AlertDialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.widget.Button;

import android.os.Bundle;
import android.widget.EditText;
import android.view.View;
import android.widget.Toast;
import java.util.List;

import edu.gatech.seclass.jobcompare6300.DataManager;
import edu.gatech.seclass.jobcompare6300.database.AdjustWeightDAO;
import edu.gatech.seclass.jobcompare6300.model.JobWeightSettings;
import edu.gatech.seclass.jobcompare6300.model.MyDialog;

public class AdjustComparisonSettings extends AppCompatActivity {
    EditText YearlySalaryWeightEntry;
    EditText yearlyBonusWeightEntry;
    EditText numberOfStockWeightEntry;
    EditText homeFundWeightEntry;
    EditText holidayWeightEntry;
    EditText internetStipendWeightEntry;
    EditText Entry_Text;


    protected void onCreate(Bundle savedInstanceState) {

        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_weight_settings); // Use the correct layout file for your main activity
        AdjustWeightDAO dao = new AdjustWeightDAO(this);

        // Get the current settings from the database or null if they don't exist
        JobWeightSettings currentSettings = dao.getJobWeight();

        // Define default values
        int defaultYearlySalaryWeight = 1;

        // Initialize EditText fields
        YearlySalaryWeightEntry = findViewById(R.id.Yearly_Salary_weight);
        yearlyBonusWeightEntry = findViewById(R.id.Yearly_Bonus_weight);
        numberOfStockWeightEntry = findViewById(R.id.Number_Stock_weight);
        homeFundWeightEntry = findViewById(R.id.Home_Buying_weight);
        holidayWeightEntry = findViewById(R.id.Holidays_weight);
        internetStipendWeightEntry = findViewById(R.id.Internet_weight);


        // Set the EditText fields to the current settings or default values
        YearlySalaryWeightEntry.setText(currentSettings != null ? String.valueOf(currentSettings.getAYS()) : String.valueOf(defaultYearlySalaryWeight));
        yearlyBonusWeightEntry.setText(currentSettings != null ? String.valueOf(currentSettings.getAYB()) : String.valueOf(defaultYearlySalaryWeight));
        numberOfStockWeightEntry.setText(currentSettings != null ? String.valueOf(currentSettings.getCSO()) : String.valueOf(defaultYearlySalaryWeight));
        homeFundWeightEntry.setText(currentSettings != null ? String.valueOf(currentSettings.getHBP()) : String.valueOf(defaultYearlySalaryWeight));
        holidayWeightEntry.setText(currentSettings != null ? String.valueOf(currentSettings.getPCH()) : String.valueOf(defaultYearlySalaryWeight));
        internetStipendWeightEntry.setText(currentSettings != null ? String.valueOf(currentSettings.getMIS()) : String.valueOf(defaultYearlySalaryWeight));


        findViewById(R.id.save_weight).setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {

                if (saveWeight()) {
                    AlertDialog.Builder builder = new AlertDialog.Builder(AdjustComparisonSettings.this);

                    builder.setMessage("Settings saved");
                    builder.setPositiveButton(R.string.ok, new DialogInterface.OnClickListener() {
                        @Override
                        public void onClick(DialogInterface dialog, int which) {
                            // No need to call finish() if you want the back stack to be handled normally,
                            // unless you have a specific reason to remove the current activity from the back stack.
                            Intent intent = new Intent(AdjustComparisonSettings.this, MainActivity.class);
                            startActivity(intent);
                        }
                    });

                    builder.show();

                }

            }
        });

        findViewById(R.id.cancel_weight).setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(AdjustComparisonSettings.this, MainActivity.class);
                startActivity(intent);
            }
        });


    }

    private boolean validateAndSetError(EditText editText, String fieldName) {
        String inputStr = editText.getText().toString();
        try {
            float value = Float.parseFloat(inputStr);
            if (value < 0 || value>10) {
                MyDialog.showDialogNotice(this, "The weight setting should be from 0 to 10.");
                return false;
            }
        } catch (NumberFormatException e) {
            MyDialog.showDialogNotice(this, "Must be a numeric value.");

            return false;
        }
        return true;
    }

        private boolean saveWeight() {
            boolean isValid = true;

            // Validate each field individually
            isValid &= validateAndSetError(YearlySalaryWeightEntry, "Yearly Salary Weight");
            isValid &= validateAndSetError(yearlyBonusWeightEntry, "Yearly Bonus Weight");
            isValid &= validateAndSetError(numberOfStockWeightEntry, "Number of Stock Weight");
            isValid &= validateAndSetError(homeFundWeightEntry, "Home Fund Weight");
            isValid &= validateAndSetError(holidayWeightEntry, "Holiday Weight");
            isValid &= validateAndSetError(internetStipendWeightEntry, "Internet Stipend Weight");

            // Proceed only if all inputs are valid
            if (isValid) {
                int YearlySalaryWeight = Integer.parseInt(YearlySalaryWeightEntry.getText().toString());
                int YearlyBonusWeight = Integer.parseInt(yearlyBonusWeightEntry.getText().toString());
                int numberOfStockWeight =Integer.parseInt(numberOfStockWeightEntry.getText().toString());
                int homeFundWeight = Integer.parseInt(homeFundWeightEntry.getText().toString());
                int holidayWeight = Integer.parseInt(holidayWeightEntry.getText().toString());
                int internetStipendWeight = Integer.parseInt(internetStipendWeightEntry.getText().toString());

                JobWeightSettings settings = new JobWeightSettings();
                settings.setAYS(YearlySalaryWeight);
                settings.setAYB(YearlyBonusWeight);
                settings.setCSO(numberOfStockWeight);
                settings.setHBP(homeFundWeight);
                settings.setPCH(holidayWeight);
                settings.setMIS(internetStipendWeight);

                AdjustWeightDAO dao = new AdjustWeightDAO(this);
                dao.addOrUpdateJobWeightSettings(settings);

                return true;
            }
            else{
                return false;
            }
        }


}


