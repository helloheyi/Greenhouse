package edu.gatech.seclass.jobcompare6300.ui;

import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.TextView;

import java.util.ArrayList;
import java.util.List;

import edu.gatech.seclass.jobcompare6300.R;
import edu.gatech.seclass.jobcompare6300.database.OfferDetailDAO;
import edu.gatech.seclass.jobcompare6300.model.OfferDetail;

public class CompareOffersActivity extends AppCompatActivity {

    TextView  title1, title2, company1, company2, city1, city2, state1, state2, cost1, cost2,
            salary1, salary2, bonus1, bonus2, stock1, stock2, homeFund1, homeFund2, holidays1,
            holidays2, internetStipend1, internetStipend2;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_compare_offers);

        OfferDetail offer1 = (OfferDetail) getIntent().getSerializableExtra("offer1");
        OfferDetail offer2 = (OfferDetail) getIntent().getSerializableExtra("offer2");;

        title1 = findViewById(R.id.title1);
        title2 = findViewById(R.id.title2);
        company1 = findViewById(R.id.company1);
        company2 = findViewById(R.id.company2);
        city1 = findViewById(R.id.city1);
        city2 = findViewById(R.id.city2);
        state1 = findViewById(R.id.state1);
        state2 = findViewById(R.id.state2);
        salary1 = findViewById(R.id.salary1);
        salary2 = findViewById(R.id.salary2);
        bonus1 = findViewById(R.id.bonus1);
        bonus2 = findViewById(R.id.bonus2);
        stock1 = findViewById(R.id.stock1);
        stock2 = findViewById(R.id.stock2);
        homeFund1 = findViewById(R.id.homeFund1);
        homeFund2 = findViewById(R.id.homeFund2);
        holidays1 = findViewById(R.id.holiday1);
        holidays2 = findViewById(R.id.holiday2);
        internetStipend1 = findViewById(R.id.internetStipend1);
        internetStipend2 = findViewById(R.id.internetStipend2);

        title1.setText(offer1.getTitle());
        title2.setText(offer2.getTitle());
        company1.setText(offer1.getName());
        company2.setText(offer2.getName());
        city1.setText(offer1.getLocation().city);
        city2.setText(offer2.getLocation().city);
        state1.setText(offer1.getLocation().state);
        state2.setText(offer2.getLocation().state);
        salary1.setText(String.valueOf(offer1.getSalary() / offer1.getLocation().costOfLiving * 100));
        salary2.setText(String.valueOf(offer2.getSalary() / offer2.getLocation().costOfLiving * 100));
        bonus1.setText(String.valueOf(offer1.getBonus() / offer1.getLocation().costOfLiving * 100));
        bonus2.setText(String.valueOf(offer2.getBonus() / offer2.getLocation().costOfLiving * 100));
        stock1.setText(String.valueOf(offer1.getStockOptions()));
        stock2.setText(String.valueOf(offer2.getStockOptions()));
        homeFund1.setText(String.valueOf(offer1.getBenefits().getHomeProgramFund()));
        homeFund2.setText(String.valueOf(offer2.getBenefits().getHomeProgramFund()));
        holidays1.setText(String.valueOf(offer1.getBenefits().getHolidays()));
        holidays2.setText(String.valueOf(offer2.getBenefits().getHolidays()));
        internetStipend1.setText(String.valueOf(offer1.getBenefits().getInternetStipend()));
        internetStipend2.setText(String.valueOf(offer2.getBenefits().getInternetStipend()));

        findViewById(R.id.btnReturn).setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                finish();
            }
        });
    }

    public void btnMainHandleClick(View view) {
        if (view.getId() == R.id.btnMain) {
            Intent intent = new Intent(this, MainActivity.class);
            startActivity(intent);
        }
    }
}