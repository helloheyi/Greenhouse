package edu.gatech.seclass.jobcompare6300.ui;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import static edu.gatech.seclass.jobcompare6300.DataManager.DATABASE_OFFER;

import androidx.appcompat.app.AppCompatActivity;

import android.app.AlertDialog;
import android.content.DialogInterface;
import android.os.Bundle;
import android.text.Editable;
import android.text.TextUtils;
import android.text.TextWatcher;
import android.util.Log;
import android.view.Gravity;
import android.widget.EditText;
import android.view.View;
import android.widget.TextView;

import java.util.List;

import edu.gatech.seclass.jobcompare6300.DataManager;
import edu.gatech.seclass.jobcompare6300.R;
import edu.gatech.seclass.jobcompare6300.database.OfferDetailDAO;
import edu.gatech.seclass.jobcompare6300.model.MoneyTextWatcher;
import edu.gatech.seclass.jobcompare6300.model.MyDialog;
import edu.gatech.seclass.jobcompare6300.model.OfferDetail;

public class AddOffersActivity extends AppCompatActivity {

    EditText pageTitleEntry;
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
    SharedPreferences preferences;
    SharedPreferences.Editor editor;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_add_offers);

        preferences = getSharedPreferences("add_offers", MODE_PRIVATE);
        editor = preferences.edit();

        titleEntry = findViewById(R.id.titleId);
        companyEntry = findViewById(R.id.companyId);
        cityEntry = findViewById(R.id.cityId);
        stateEntry = findViewById(R.id.stateId);
        costOfLivingEntry = findViewById(R.id.costOfLivingId);
        yearlySalaryEntry = findViewById(R.id.yearlySalaryId);
        yearlyBonusEntry = findViewById(R.id.yearlyBonusId);
        numberOfStockEntry = findViewById(R.id.numberOfStockId);
        homeFundEntry = findViewById(R.id.homeFundId);
        holidayEntry = findViewById(R.id.holidayId);
        internetStipendEntry = findViewById(R.id.internetStipendId);

        titleEntry.addTextChangedListener(textWatcher);
        companyEntry.addTextChangedListener(textWatcher);
        cityEntry.addTextChangedListener(textWatcher);
        stateEntry.addTextChangedListener(textWatcher);
        costOfLivingEntry.addTextChangedListener(textWatcher);
        yearlySalaryEntry.addTextChangedListener(textWatcher);
        yearlyBonusEntry.addTextChangedListener(textWatcher);
        numberOfStockEntry.addTextChangedListener(textWatcher);
        homeFundEntry.addTextChangedListener(textWatcher);
        holidayEntry.addTextChangedListener(textWatcher);

        yearlySalaryEntry.addTextChangedListener(new MoneyTextWatcher(yearlySalaryEntry));
        yearlyBonusEntry.addTextChangedListener(new MoneyTextWatcher(yearlyBonusEntry));
        homeFundEntry.addTextChangedListener(new MoneyTextWatcher(homeFundEntry));
        internetStipendEntry.addTextChangedListener(new MoneyTextWatcher(internetStipendEntry));
        setCostOfLivingInputWatcher();
        setHolidaysInputWatcher();

        if(preferences != null) {
            String title = preferences.getString("titleEntry", "");
            titleEntry.setText(title);
            String company = preferences.getString("companyEntry", "");
            companyEntry.setText(company);
            String city = preferences.getString("cityEntry", "");
            cityEntry.setText(city);
            String state = preferences.getString("stateEntry", "");
            stateEntry.setText(state);
            String costOfLiving = preferences.getString("costOfLivingEntry", "");
            costOfLivingEntry.setText(costOfLiving);
            String yearlySalary = preferences.getString("yearlySalaryEntry", "");
            yearlySalaryEntry.setText(yearlySalary);
            String yearlyBonus = preferences.getString("yearlyBonusEntry", "");
            yearlyBonusEntry.setText(yearlyBonus);
            String numberOfStock = preferences.getString("numberOfStockEntry", "");
            numberOfStockEntry.setText(numberOfStock);
            String homeFund = preferences.getString("homeFundEntry", "");
            homeFundEntry.setText(homeFund);
            String holiday = preferences.getString("holidayEntry", "");
            holidayEntry.setText(holiday);
            String internetStipend = preferences.getString("internetStipendEntry", "");
            internetStipendEntry.setText(internetStipend);
        }

        findViewById(R.id.buttonSave).setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                OfferDetail offer = addAnOffer();
                if(offer != null){
                    showMessage(R.string.save_successfully, offer);
                }
            }
        });

        findViewById(R.id.btnReturn).setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                finish();
            }
        });

        findViewById(R.id.buttonDelete).setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                int deletedRows = DataManager.getOfferDetailDAO().deleteByFlag(DATABASE_OFFER);
                if(deletedRows != 0){
                    DataManager.getOffersList().clear();
                    MyDialog.showDialogNotice(AddOffersActivity.this, getString(R.string.deleted_all_offers));
                }
                else{
                    MyDialog.showDialogNotice(AddOffersActivity.this, getString(R.string.nothing_to_delete));
                }
            }
        });

    }

    private OfferDetail addAnOffer() {
        String title = titleEntry.getText().toString();
        if (TextUtils.isEmpty(title)){
            MyDialog.showDialogNotice(this, getString(R.string.empty_field));
            return null;
        }

        String company = companyEntry.getText().toString();
        if (TextUtils.isEmpty(company)){
            MyDialog.showDialogNotice(this, getString(R.string.empty_field));
            return null;
        }

        String city = cityEntry.getText().toString();
        if (TextUtils.isEmpty(city)){
            MyDialog.showDialogNotice(this, getString(R.string.empty_field));
            return null;
        }

        String state = stateEntry.getText().toString();
        if (TextUtils.isEmpty(state)){
            MyDialog.showDialogNotice(this, getString(R.string.empty_field));
            return null;
        }

        String costOfLiving = costOfLivingEntry.getText().toString();
        if (TextUtils.isEmpty(costOfLiving)){
            MyDialog.showDialogNotice(this, getString(R.string.empty_field));
            return null;
        }
        float cost = Float.parseFloat(costOfLiving);
        if (cost > 250) {
            MyDialog.showDialogNotice(this, getString(R.string.cost_index_limit));
            return null;
        }

        String strSalary = yearlySalaryEntry.getText().toString();
        if (TextUtils.isEmpty(strSalary)){
            MyDialog.showDialogNotice(this, getString(R.string.empty_field));
            return null;
        }
        float salary = Float.parseFloat(strSalary);
        if (salary > Float.MAX_VALUE) {
            MyDialog.showDialogNotice(this, getString(R.string.amount_limit));
            return null;
        }

        String strBonus = yearlyBonusEntry.getText().toString();
        if (TextUtils.isEmpty(strBonus)){
            MyDialog.showDialogNotice(this, getString(R.string.empty_field));
            return null;
        }
        float bonus = Float.parseFloat(strBonus);
        if (bonus > Float.MAX_VALUE) {
            MyDialog.showDialogNotice(this, getString(R.string.amount_limit));
            return null;
        }

        String strStock = numberOfStockEntry.getText().toString();
        if (TextUtils.isEmpty(strStock)){
            MyDialog.showDialogNotice(this, getString(R.string.empty_field));
            return null;
        }
        int stock = Integer.parseInt(strStock);
        if (stock > Integer.MAX_VALUE) {
            MyDialog.showDialogNotice(this, getString(R.string.amount_limit));
            return null;
        }

        String strHome = homeFundEntry.getText().toString();
        if (TextUtils.isEmpty(strHome)){
            MyDialog.showDialogNotice(this, getString(R.string.empty_field));
            return null;
        }
        float homeFund = Float.parseFloat(strHome);
        if (homeFund > 0.15 * salary) {
            MyDialog.showDialogNotice(this, getString(R.string.home_fund_limit));
            return null;
        }

        String strHoliday = holidayEntry.getText().toString();
        if (TextUtils.isEmpty(strHoliday)){
            MyDialog.showDialogNotice(this, getString(R.string.empty_field));
            return null;
        }
        float holiday = Float.parseFloat(strHoliday);
        if (holiday > 20) {
            MyDialog.showDialogNotice(this, getString(R.string.holiday_limit));
            return null;
        }

        String strInternet = internetStipendEntry.getText().toString();
        if (TextUtils.isEmpty(strInternet)){
            MyDialog.showDialogNotice(this, getString(R.string.empty_field));
            return null;
        }
        float internet = Float.parseFloat(strInternet);
        if (internet < 0 || internet > 75) {
            MyDialog.showDialogNotice(this, getString(R.string.internet_stipend_limit));
            return null;
        }

        // Create offer
        OfferDetail offer = DataManager.addOffer(title, company, city, state,
                cost, salary, bonus, stock, homeFund, holiday, internet);

        // Add to db and array
        if(offer != null && DataManager.getOffersList() != null){
            for(OfferDetail existingOffer : DataManager.getOffersList()){
                if(existingOffer.getTitle().equals(offer.getTitle()) &&
                        existingOffer.getName().equals(offer.getName()) &&
                        existingOffer.getLocation().city.equals(offer.getLocation().city) &&
                        existingOffer.getLocation().state.equals(offer.getLocation().state)){
                    MyDialog.showDialogNotice(this, getString(R.string.offer_exists));
                    return null;
                }
            }
        }
        if(offer != null && DataManager.getCurrentJob() != null){
            OfferDetail currentJob = DataManager.getCurrentJob();
            if(currentJob.getTitle().equals(offer.getTitle()) &&
                    currentJob.getName().equals(offer.getName()) &&
                    currentJob.getLocation().city.equals(offer.getLocation().city) &&
                    currentJob.getLocation().state.equals(offer.getLocation().state)){
                MyDialog.showDialogNotice(this, getString(R.string.matches_cur_job));
                return null;
            }
        }
        if(offer != null){
            DataManager.addToOffersList(offer);
            DataManager.getOfferDetailDAO().add(offer, DATABASE_OFFER);
        }

        titleEntry.setText("");
        companyEntry.setText("");
        cityEntry.setText("");
        stateEntry.setText("");
        costOfLivingEntry.setText("");
        yearlySalaryEntry.setText("");
        yearlyBonusEntry.setText("");
        numberOfStockEntry.setText("");
        homeFundEntry.setText("");
        holidayEntry.setText("");
        internetStipendEntry.setText("");

        return offer;
    }

    private void showMessage(int id, OfferDetail offer) {
        AlertDialog.Builder builder = new AlertDialog.Builder(this);

        TextView title = new TextView(this);
        title.setGravity(Gravity.CENTER);
        title.setTextSize(24);
        title.setPadding(0,10,0,10);

        String uiButton = this.getString(R.string.ok);
        if(DataManager.getCurrentJob() != null && offer != null){
            uiButton = this.getString(R.string.no);
        }
        builder.setPositiveButton(uiButton, new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialog, int which) {
                dialog.dismiss();
            }
        });

        if(DataManager.getCurrentJob() != null && offer != null) {
            builder.setMessage(R.string.compare_with_job);
            title.setText(id);
            builder.setNegativeButton(this.getString(R.string.yes), new DialogInterface.OnClickListener() {
                @Override
                public void onClick(DialogInterface dialogInterface, int i) {
                    Intent intent = new Intent(AddOffersActivity.this, CompareOffersActivity.class);
                    intent.putExtra("offer1", DataManager.getCurrentJob());
                    intent.putExtra("offer2", offer);
                    AddOffersActivity.this.startActivity(intent);
                }
            });
        }
        else{
            title.setText(R.string.notice);
            builder.setMessage(R.string.save_successfully);
        }
        builder.setCustomTitle(title);

        builder.show();
    }

    TextWatcher textWatcher = new TextWatcher() {
        @Override
        public void beforeTextChanged(CharSequence charSequence, int i, int i1, int i2) {

        }

        @Override
        public void onTextChanged(CharSequence charSequence, int i, int i1, int i2) {

        }

        @Override
        public void afterTextChanged(Editable editable) {
            if(editable == titleEntry.getEditableText()){
                editor.putString("titleEntry", titleEntry.getText().toString());
            }
            else if(editable == companyEntry.getEditableText()){
                editor.putString("companyEntry", companyEntry.getText().toString());
            }
            else if(editable == cityEntry.getEditableText()){
                editor.putString("cityEntry", cityEntry.getText().toString());
            }
            else if(editable == stateEntry.getEditableText()){
                editor.putString("stateEntry", stateEntry.getText().toString());
            }
            else if(editable == costOfLivingEntry.getEditableText()){
                editor.putString("costOfLivingEntry", costOfLivingEntry.getText().toString());
            }
            else if(editable == yearlySalaryEntry.getEditableText()){
                editor.putString("yearlySalaryEntry", yearlySalaryEntry.getText().toString());
            }
            else if(editable == yearlyBonusEntry.getEditableText()){
                editor.putString("yearlyBonusEntry", yearlyBonusEntry.getText().toString());
            }
            else if(editable == numberOfStockEntry.getEditableText()){
                editor.putString("numberOfStockEntry", numberOfStockEntry.getText().toString());
            }
            else if(editable == homeFundEntry.getEditableText()){
                editor.putString("homeFundEntry", homeFundEntry.getText().toString());
            }
            else if(editable == holidayEntry.getEditableText()){
                editor.putString("holidayEntry", holidayEntry.getText().toString());
            }
            else if(editable == internetStipendEntry.getEditableText()){
                editor.putString("internetStipendEntry", internetStipendEntry.getText().toString());
            }
            editor.apply();
        }
    };

    private void setCostOfLivingInputWatcher() {
        costOfLivingEntry.addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence s, int start, int count, int after) {

            }

            @Override
            public void onTextChanged(CharSequence s, int start, int before, int count) {
                if (s.length() > 0) {
                    int number = Integer.parseInt(s.toString());
                    if (number < 0 || number > 250) {
                        MyDialog.showDialogNotice(AddOffersActivity.this, getString(R.string.cost_index_limit));
                    }
                }
            }

            @Override
            public void afterTextChanged(Editable s) {

            }
        });
    }

    private void setHolidaysInputWatcher() {
        holidayEntry.addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence s, int start, int count, int after) {

            }

            @Override
            public void onTextChanged(CharSequence s, int start, int before, int count) {
                if (s.length() > 0) {
                    float number = Float.parseFloat(s.toString());
                    if (number < 0 || number > 20) {
                        MyDialog.showDialogNotice(AddOffersActivity.this, getString(R.string.holiday_limit));
                    }
                }
            }

            @Override
            public void afterTextChanged(Editable s) {

            }
        });
    }

}