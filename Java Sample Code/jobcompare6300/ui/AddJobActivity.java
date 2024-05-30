package edu.gatech.seclass.jobcompare6300.ui;

import androidx.appcompat.app.AppCompatActivity;

import android.app.AlertDialog;
import android.content.DialogInterface;
import android.graphics.Color;
import android.os.Bundle;
import android.text.Editable;
import android.text.TextUtils;
import android.text.TextWatcher;
import android.view.View;
import android.widget.EditText;
import android.widget.TextView;

import java.util.regex.Matcher;
import java.util.regex.Pattern;

import edu.gatech.seclass.jobcompare6300.DataManager;
import edu.gatech.seclass.jobcompare6300.R;
import edu.gatech.seclass.jobcompare6300.model.MoneyTextWatcher;
import edu.gatech.seclass.jobcompare6300.model.MyDialog;
import edu.gatech.seclass.jobcompare6300.model.OfferDetail;

public class AddJobActivity extends AppCompatActivity {

    TextView pageTitleEntry;
    EditText titleEntry;
    EditText companyEntry;
    EditText cityEntry;
    EditText stateEntry;
    EditText costOfLivingEntry;
    EditText yearlySalaryEntry;
    EditText yearlyBonusEntry;
    EditText numberOfStockEntry;
    EditText homeFundEntry;
    EditText holidayEntry;
    EditText internetStipendEntry;

    private boolean isReturn = false;

    private final String REGEX_0_TO_250 = "^([0-9]|[1-9][0-9]|1[0-9][0-9]|200|250)$";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_add_job);

        // Change the page title for editing the current job, and show the current job info on the screen
        String addOrEdit = getIntent().getSerializableExtra(MainActivity.KEY_ADD_OR_EDIT, String.class);
        if (MainActivity.KEY_EDIT_JOB.equals(addOrEdit)) {
            setCurrentJobInfo();
        }

        setCostOfLivingInputWatcher();

        yearlySalaryEntry = findViewById(R.id.yearlySalaryId);
        yearlySalaryEntry.addTextChangedListener(new MoneyTextWatcher(yearlySalaryEntry));

        yearlyBonusEntry = findViewById(R.id.yearlyBonusId);
        yearlyBonusEntry.addTextChangedListener(new MoneyTextWatcher(yearlyBonusEntry));

        homeFundEntry = findViewById(R.id.homeFundId);
        homeFundEntry.addTextChangedListener(new MoneyTextWatcher(homeFundEntry));

        setHolidaysInputWatcher();

        internetStipendEntry = findViewById(R.id.internetStipendId);
        internetStipendEntry.addTextChangedListener(new MoneyTextWatcher(internetStipendEntry));

        findViewById(R.id.buttonSave).setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                boolean result = saveJob();
                if (result) {
                    showDialogAndClose();
                }
            }
        });

        findViewById(R.id.btnReturn).setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                isReturn = true;
                finish();
            }
        });
    }

    @Override
    protected void onPause() {
        super.onPause();
    }

    @Override
    protected void onStop() {
        super.onStop();

        // If the user click "Cancel", the info won't be stored to db
        if (!isReturn) {
            // Save the unsaved info to db
            saveJobWithUncompletedInfo();
        }
    }

    private void setCostOfLivingInputWatcher() {
        costOfLivingEntry = findViewById(R.id.costOfLivingId);
        costOfLivingEntry.addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence s, int start, int count, int after) {

            }

            @Override
            public void onTextChanged(CharSequence s, int start, int before, int count) {
                if (s.length() > 0) {
                    int number = Integer.parseInt(s.toString());
                    if (number < 0 || number > 250) {
                        MyDialog.showDialogNotice(AddJobActivity.this, getString(R.string.cost_index_limit));
                    }
                }

//                Pattern p = Pattern.compile(REGEX_0_TO_250);
//                Matcher m  = p.matcher(s.toString());
//                if (!m.matches()) {
//                    MyDialog.showDialogNotice(AddJobActivity.this, getString(R.string.cost_index_limit));
//                }
            }

            @Override
            public void afterTextChanged(Editable s) {

            }
        });
    }


    private void setHolidaysInputWatcher() {
        holidayEntry = findViewById(R.id.holidayId);
        holidayEntry.addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence s, int start, int count, int after) {

            }

            @Override
            public void onTextChanged(CharSequence s, int start, int before, int count) {
                if (s.length() > 0) {
                    float number = Float.parseFloat(s.toString());
                    if (number < 0 || number > 20) {
                        MyDialog.showDialogNotice(AddJobActivity.this, getString(R.string.holiday_limit));
                    }
                }
            }

            @Override
            public void afterTextChanged(Editable s) {

            }
        });
    }


    /**
     * Fill in the blanks and save the job info
     * @return whether it is saved successfully
     */
    private boolean saveJob() {

        titleEntry = findViewById(R.id.titleId);
        String title = titleEntry.getText().toString();
        if (TextUtils.isEmpty(title)){
            MyDialog.showDialogNotice(this, getString(R.string.empty_field));
            return false;
        }

        companyEntry = findViewById(R.id.companyId);
        String company = companyEntry.getText().toString();
        if (TextUtils.isEmpty(company)){
            MyDialog.showDialogNotice(this, getString(R.string.empty_field));
            return false;
        }

        cityEntry = findViewById(R.id.cityId);
        String city = cityEntry.getText().toString();
        if (TextUtils.isEmpty(city)){
            MyDialog.showDialogNotice(this, getString(R.string.empty_field));
            return false;
        }

        stateEntry = findViewById(R.id.stateId);
        String state = stateEntry.getText().toString();
        if (TextUtils.isEmpty(state)){
            MyDialog.showDialogNotice(this, getString(R.string.empty_field));
            return false;
        }

        costOfLivingEntry = findViewById(R.id.costOfLivingId);
        String costOfLiving = costOfLivingEntry.getText().toString();
        if (TextUtils.isEmpty(costOfLiving)){
            MyDialog.showDialogNotice(this, getString(R.string.empty_field));
            return false;
        }
        float cost = Float.parseFloat(costOfLiving);
        if (cost > 250) {
            MyDialog.showDialogNotice(this, getString(R.string.cost_index_limit));
            return false;
        }

        yearlySalaryEntry = findViewById(R.id.yearlySalaryId);
        String strSalary = yearlySalaryEntry.getText().toString();
        if (TextUtils.isEmpty(strSalary)){
            MyDialog.showDialogNotice(this, getString(R.string.empty_field));
            return false;
        }
        float salary = Float.parseFloat(strSalary);
        if (salary > Float.MAX_VALUE) {
            MyDialog.showDialogNotice(this, getString(R.string.amount_limit));
            return false;
        }

        yearlyBonusEntry = findViewById(R.id.yearlyBonusId);
        String strBonus = yearlyBonusEntry.getText().toString();
        if (TextUtils.isEmpty(strBonus)){
            MyDialog.showDialogNotice(this, getString(R.string.empty_field));
            return false;
        }
        float bonus = Float.parseFloat(strBonus);
        if (bonus > Float.MAX_VALUE) {
            MyDialog.showDialogNotice(this, getString(R.string.amount_limit));
            return false;
        }

        numberOfStockEntry = findViewById(R.id.numberOfStockId);
        String strStock = numberOfStockEntry.getText().toString();
        if (TextUtils.isEmpty(strStock)){
            MyDialog.showDialogNotice(this, getString(R.string.empty_field));
            return false;
        }
        int stock = Integer.parseInt(strStock);
        if (stock > Integer.MAX_VALUE) {
            MyDialog.showDialogNotice(this, getString(R.string.amount_limit));
            return false;
        }

        homeFundEntry = findViewById(R.id.homeFundId);
        String strHome = homeFundEntry.getText().toString();
        if (TextUtils.isEmpty(strHome)){
            MyDialog.showDialogNotice(this, getString(R.string.empty_field));
            return false;
        }
        float homeFund = Float.parseFloat(strHome);
        if (homeFund > 0.15 * salary) {
            MyDialog.showDialogNotice(this, getString(R.string.home_fund_limit));
            return false;
        }

        holidayEntry = findViewById(R.id.holidayId);
        String strHoliday = holidayEntry.getText().toString();
        if (TextUtils.isEmpty(strHoliday)){
            MyDialog.showDialogNotice(this, getString(R.string.empty_field));
            return false;
        }
        float holiday = Float.parseFloat(strHoliday);
        if (holiday > 20) {
            MyDialog.showDialogNotice(this, getString(R.string.holiday_limit));
            return false;
        }

        internetStipendEntry = findViewById(R.id.internetStipendId);
        String strInternet = internetStipendEntry.getText().toString();
        if (TextUtils.isEmpty(strInternet)){
            MyDialog.showDialogNotice(this, getString(R.string.empty_field));
            return false;
        }
        float internet = Float.parseFloat(strInternet);
        if (internet < 0 || internet > 75) {
            MyDialog.showDialogNotice(this, getString(R.string.internet_stipend_limit));
            return false;
        }

        OfferDetail offer;
        if (DataManager.getCurrentJob() == null) { // add a job
            offer = DataManager.addOffer(title, company, city, state, cost,
                    salary, bonus, stock, homeFund, holiday, internet);

            // Update currentJob
            DataManager.setCurrentJob(offer);

            // Add current job to db
            if (offer != null) {
                DataManager.getOfferDetailDAO().add(offer, DataManager.DATABASE_JOB);
            }
        } else { // edit the job
            boolean result = DataManager.editOffer(title, company, city, state, cost,
                    salary, bonus, stock, homeFund, holiday, internet);
            if (!result) {
                return false;
            }

            // As every field of the job info can be edit, the system will delete the old item and insert the current one.
            int deletedRows = DataManager.getOfferDetailDAO().deleteByFlag(DataManager.DATABASE_JOB);
            if (deletedRows != 0) {
                DataManager.getOfferDetailDAO().add(DataManager.getCurrentJob(), DataManager.DATABASE_JOB);
            }
        }
        return true;
    }

    private void setCurrentJobInfo() {
        pageTitleEntry = findViewById(R.id.currentJobTitleId);
        pageTitleEntry.setText(R.string.edit_current_job);

        titleEntry = findViewById(R.id.titleId);
        titleEntry.setText(DataManager.getCurrentJob().getTitle());

        companyEntry = findViewById(R.id.companyId);
        companyEntry.setText(DataManager.getCurrentJob().getName());

        cityEntry = findViewById(R.id.cityId);
        cityEntry.setText(DataManager.getCurrentJob().getLocation().city);

        stateEntry = findViewById(R.id.stateId);
        stateEntry.setText(DataManager.getCurrentJob().getLocation().state);

        costOfLivingEntry = findViewById(R.id.costOfLivingId);
        float cost = DataManager.getCurrentJob().getLocation().costOfLiving;
        if (cost != 0) {
            costOfLivingEntry.setText(String.valueOf(Math.round(cost)));
        }

        yearlySalaryEntry = findViewById(R.id.yearlySalaryId);
        float salary = DataManager.getCurrentJob().getSalary();
        if (salary != 0) {
            yearlySalaryEntry.setText(String.valueOf(salary));
        }

        yearlyBonusEntry = findViewById(R.id.yearlyBonusId);
        float bonus = DataManager.getCurrentJob().getBonus();
        if (bonus != 0) {
            yearlyBonusEntry.setText(String.valueOf(bonus));
        }

        numberOfStockEntry = findViewById(R.id.numberOfStockId);
        int stock = DataManager.getCurrentJob().getStockOptions();
        if (stock != 0) {
            numberOfStockEntry.setText(String.valueOf(stock));
        }

        homeFundEntry = findViewById(R.id.homeFundId);
        float homeFund = DataManager.getCurrentJob().getBenefits().getHomeProgramFund();
        if (homeFund != 0) {
            homeFundEntry.setText(String.valueOf(homeFund));
        }

        holidayEntry = findViewById(R.id.holidayId);
        float holiday = DataManager.getCurrentJob().getBenefits().getHolidays();
        if (holiday != 0) {
            holidayEntry.setText(String.valueOf(holiday));
        }

        internetStipendEntry = findViewById(R.id.internetStipendId);
        float internet = DataManager.getCurrentJob().getBenefits().getInternetStipend();
        if (internet != 0) {
            internetStipendEntry.setText(String.valueOf(internet));
        }
    }

    private void showDialogAndClose() {
        AlertDialog.Builder builder = new AlertDialog.Builder(this);

        builder.setMessage(R.string.save_successfully);
        builder.setPositiveButton(R.string.ok, new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialog, int which) {
                finish();
            }
        });

        builder.show();
    }

    /*
    private void clearBackground() {
        titleEntry = findViewById(R.id.titleId);
        companyEntry.setBackgroundColor(Color.TRANSPARENT);

        companyEntry = findViewById(R.id.companyId);
        companyEntry.setBackgroundColor(Color.TRANSPARENT);

        cityEntry = findViewById(R.id.cityId);
        cityEntry.setBackgroundColor(Color.TRANSPARENT);

        stateEntry = findViewById(R.id.stateId);
        stateEntry.setBackgroundColor(Color.TRANSPARENT);

        costOfLivingEntry = findViewById(R.id.costOfLivingId);
        costOfLivingEntry.setBackgroundColor(Color.TRANSPARENT);

        yearlySalaryEntry = findViewById(R.id.yearlySalaryId);
        yearlySalaryEntry.setBackgroundColor(Color.TRANSPARENT);

        yearlyBonusEntry = findViewById(R.id.yearlyBonusId);
        yearlyBonusEntry.setBackgroundColor(Color.TRANSPARENT);

        numberOfStockEntry = findViewById(R.id.numberOfStockId);
        numberOfStockEntry.setBackgroundColor(Color.TRANSPARENT);

        homeFundEntry = findViewById(R.id.homeFundId);
        homeFundEntry.setBackgroundColor(Color.TRANSPARENT);

        holidayEntry = findViewById(R.id.holidayId);
        holidayEntry.setBackgroundColor(Color.TRANSPARENT);

        internetStipendEntry = findViewById(R.id.internetStipendId);
        internetStipendEntry.setBackgroundColor(Color.TRANSPARENT);
    }
    */

    /**
     * Save the uncompleted job info to db
     */
    private void saveJobWithUncompletedInfo() {

        titleEntry = findViewById(R.id.titleId);
        String title = titleEntry.getText().toString();

        companyEntry = findViewById(R.id.companyId);
        String company = companyEntry.getText().toString();

        cityEntry = findViewById(R.id.cityId);
        String city = cityEntry.getText().toString();

        stateEntry = findViewById(R.id.stateId);
        String state = stateEntry.getText().toString();

        costOfLivingEntry = findViewById(R.id.costOfLivingId);
        String costOfLiving = costOfLivingEntry.getText().toString();
        float cost = 0;
        if (!TextUtils.isEmpty(costOfLiving)){
            cost = Float.parseFloat(costOfLiving);
        }

        yearlySalaryEntry = findViewById(R.id.yearlySalaryId);
        String strSalary = yearlySalaryEntry.getText().toString();
        float salary = 0;
        if (!TextUtils.isEmpty(strSalary)){
            salary = Float.parseFloat(strSalary);
        }

        yearlyBonusEntry = findViewById(R.id.yearlyBonusId);
        String strBonus = yearlyBonusEntry.getText().toString();
        float bonus = 0;
        if (!TextUtils.isEmpty(strBonus)){
            bonus = Float.parseFloat(strBonus);
        }

        numberOfStockEntry = findViewById(R.id.numberOfStockId);
        String strStock = numberOfStockEntry.getText().toString();
        int stock = 0;
        if (!TextUtils.isEmpty(strStock)){
            stock = Integer.parseInt(strStock);
        }

        homeFundEntry = findViewById(R.id.homeFundId);
        String strHome = homeFundEntry.getText().toString();
        float homeFund = 0;
        if (!TextUtils.isEmpty(strHome)){
            homeFund = Float.parseFloat(strHome);
        }

        holidayEntry = findViewById(R.id.holidayId);
        String strHoliday = holidayEntry.getText().toString();
        float holiday = 0;
        if (!TextUtils.isEmpty(strHoliday)){
            holiday = Float.parseFloat(strHoliday);
        }

        internetStipendEntry = findViewById(R.id.internetStipendId);
        String strInternet = internetStipendEntry.getText().toString();
        float internet = 0;
        if (!TextUtils.isEmpty(strInternet)){
            internet = Float.parseFloat(strInternet);
        }

        OfferDetail offer;
        if (DataManager.getCurrentJob() == null) { // add a job
            offer = DataManager.addOffer(title, company, city, state, cost,
                    salary, bonus, stock, homeFund, holiday, internet);

            // Update currentJob
            DataManager.setCurrentJob(offer);

            // Add current job to db
            if (offer != null) {
                DataManager.getOfferDetailDAO().add(offer, DataManager.DATABASE_JOB);
            }
        } else { // edit the job
            boolean result = DataManager.editOffer(title, company, city, state, cost,
                    salary, bonus, stock, homeFund, holiday, internet);

            // As every field of the job info can be edit, the system will delete the old item and insert the current one.
            int deletedRows = DataManager.getOfferDetailDAO().deleteByFlag(DataManager.DATABASE_JOB);
            if (deletedRows != 0) {
                DataManager.getOfferDetailDAO().add(DataManager.getCurrentJob(), DataManager.DATABASE_JOB);
            }
        }
    }
}