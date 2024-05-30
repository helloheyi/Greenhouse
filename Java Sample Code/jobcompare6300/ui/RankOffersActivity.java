package edu.gatech.seclass.jobcompare6300.ui;

import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;

import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
import java.util.List;

import edu.gatech.seclass.jobcompare6300.DataManager;
import edu.gatech.seclass.jobcompare6300.R;
import edu.gatech.seclass.jobcompare6300.database.OfferDetailDAO;
import edu.gatech.seclass.jobcompare6300.model.JobComparator;
import edu.gatech.seclass.jobcompare6300.model.MyDialog;
import edu.gatech.seclass.jobcompare6300.model.OfferDetail;
import edu.gatech.seclass.jobcompare6300.model.JobWeightSettings;
import edu.gatech.seclass.jobcompare6300.database.AdjustWeightDAO;

public class RankOffersActivity extends AppCompatActivity {

    private OfferDetailDAO dao;
    private List<OfferDetail> offers = new ArrayList<OfferDetail>();
    private MyAdapter adapter;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_rank_offers);

        // Get offers
        OfferDetailDAO dao = DataManager.getOfferDetailDAO();
        this.offers = dao.getOffersList();

        // Return to main menu if no offers to compare
        if (this.offers == null) {
            MyDialog.showDialogNotice(this, "No offers to compare.");
            Intent intent = new Intent(this, MainActivity.class);
            startActivity(intent);
        }

        // Add current job in ranking
        OfferDetail currentJob = dao.getCurrentJobFromDB();
        if (currentJob != null) {
            currentJob.setTitle(currentJob.getTitle() + "(Current)");
            currentJob.setName(currentJob.getName() + "(Current)");
            this.offers.add(currentJob);
        }

        // Default weights
        float AYS = 1;
        float AYB = 1;
        float CSO = 1;
        float HBP = 1;
        float PCH = 1;
        float MIS = 1;

        // Get weight settings for comparison
        AdjustWeightDAO daow = new AdjustWeightDAO(this);
        JobWeightSettings weights = daow.getJobWeight();
        if (weights != null) {
            AYS = weights.getAYS();
            AYB = weights.getAYB();
            CSO = weights.getCSO();
            HBP = weights.getHBP();
            PCH = weights.getPCH();
            MIS = weights.getMIS();
        }

        // Sort offers
        JobComparator comparator = new JobComparator(AYS, AYB, CSO, HBP, PCH, MIS);
        this.offers.sort(comparator);

        // Configure recycler view
        RecyclerView recyclerView = findViewById(R.id.recyclerview);
        recyclerView.setLayoutManager(new LinearLayoutManager(this));
        this.adapter = new MyAdapter(getApplicationContext(), this.offers);
        recyclerView.setAdapter(this.adapter);
    }

    public void btnCompareHandleClick(View view) {
        if (view.getId() == R.id.btnCompare) {
            Intent intent = new Intent(RankOffersActivity.this, CompareOffersActivity.class);
            if (this.adapter.selectedItems.size() != 2)
                MyDialog.showDialogNotice(this, "Must select exactly two offers.");
            else {
                intent.putExtra("offer1", this.offers.get(this.adapter.selectedItems.get(0)));
                intent.putExtra("offer2", this.offers.get(this.adapter.selectedItems.get(1)));
                RankOffersActivity.this.startActivity(intent);
            }
        }
    }

    public void btnReturnHandleClick(View view) {
        if (view.getId() == R.id.btnReturn) {
            Intent intent = new Intent(this, MainActivity.class);
            startActivity(intent);
        }
    }
}