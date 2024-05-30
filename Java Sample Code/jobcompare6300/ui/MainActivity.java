package edu.gatech.seclass.jobcompare6300.ui;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.widget.Button;
import android.view.View;

import edu.gatech.seclass.jobcompare6300.DataManager;
import edu.gatech.seclass.jobcompare6300.R;

public class MainActivity extends AppCompatActivity {

    DataManager dm;
    Button btnCompareOffers;

    public static final String KEY_DATA_MANAGER = "DATA_MANAGER";
    public static final String KEY_ADD_OR_EDIT = "ADD_OR_EDIT";
    public static final String KEY_ADD_JOB = "ADD_JOB";
    public static final String KEY_EDIT_JOB = "EDIT_JOB";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        dm = new DataManager(this);

        btnCompareOffers = findViewById(R.id.compareOffersButton);
        btnCompareOffers.setEnabled(false);

        // The "compare" button is disabled if no job offers were entered yet
        if ((DataManager.getCurrentJob() != null && DataManager.getCurrentJob().getName().length() >= 1 && DataManager.getOffersList() != null && DataManager.getOffersList().size() >= 1) ||
                (DataManager.getOffersList() != null && DataManager.getOffersList().size() >= 2)) {
            btnCompareOffers.setEnabled(true);
        } else {
            btnCompareOffers.setEnabled(false);
        }
    }

    @Override
    protected void onResume() {
        super.onResume();
        if ((DataManager.getCurrentJob() != null && DataManager.getCurrentJob().getName().length() >= 1 && DataManager.getOffersList() != null && DataManager.getOffersList().size() >= 1) ||
                (DataManager.getOffersList() != null && DataManager.getOffersList().size() >= 2)) {
            btnCompareOffers.setEnabled(true);
        } else {
            btnCompareOffers.setEnabled(false);
        }
    }

    @Override
    protected void onDestroy() {
        dm.exitApp();
        super.onDestroy();
    }

    // Add or edit the current job
    public void addJobHandleClick(View view) {
        if (view.getId() == R.id.addJobButton) {
            Intent intent = new Intent(this, AddJobActivity.class);

            if (DataManager.getCurrentJob() == null) {
                // Add a job
                intent.putExtra(KEY_ADD_OR_EDIT, KEY_ADD_JOB);
            } else {
                // Edit the job
                intent.putExtra(KEY_ADD_OR_EDIT, KEY_EDIT_JOB);
            }

            startActivity(intent);
        }
    }

    // Add offers
    public void addOffersHandleClick(View view) {
        if (view.getId() == R.id.addOfferButton) {
            Intent intent = new Intent(this, AddOffersActivity.class);

            startActivity(intent);
        }
    }
    // Adjust weight
    public void adjustWeightHandleClick(View view) {
        if (view.getId() == R.id.adjustSettingsButton) {
            Intent intent = new Intent(this, AdjustComparisonSettings.class);

            startActivity(intent);
        }
    }




//    public void settingHandleClick(View view) {
//        if (view.getId() == R.id.adjustSettingsButton) {
//            int result = DataManager.getOfferDetailDAO().deleteById(1);
//            // Update currentJob
//            if (result != 0) {
//                DataManager.setCurrentJob(null);
//            }
//        }
//    }

    // Rank offers
    public void compareOffersHandleClick(View view) {
        if (view.getId() == R.id.compareOffersButton) {
            Intent intent = new Intent(this, RankOffersActivity.class);

            startActivity(intent);
        }
    }

}