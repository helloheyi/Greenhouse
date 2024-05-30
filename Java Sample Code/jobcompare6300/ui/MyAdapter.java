package edu.gatech.seclass.jobcompare6300.ui;

import android.content.Context;
import android.graphics.drawable.ColorDrawable;
import android.graphics.drawable.Drawable;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.graphics.Color;
import android.widget.RelativeLayout;
import android.widget.TextView;

import java.util.ArrayList;
import java.util.List;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import edu.gatech.seclass.jobcompare6300.R;
import edu.gatech.seclass.jobcompare6300.model.OfferDetail;

public class MyAdapter extends RecyclerView.Adapter<MyAdapter.MyViewHolder> {

    Context context;
    List<OfferDetail> offers;
    public List<Integer> selectedItems = new ArrayList<>();

    public MyAdapter(Context context, List<OfferDetail> offers) {
        this.context = context;
        this.offers = offers;
    }

    @NonNull
    @Override
    public MyViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        return new MyViewHolder(LayoutInflater.from(context).inflate(R.layout.item_view,parent,false));
    }

    @Override
    public void onBindViewHolder(@NonNull MyViewHolder holder, int position) {
        holder.nameView.setText(offers.get(position).getName());
        holder.titleView.setText(offers.get(position).getTitle());
        holder.orderView.setText(String.valueOf(position+1));

        if (this.selectedItems.contains(position)) holder.rowView.setBackgroundColor(Color.GRAY);
        else holder.rowView.setBackgroundColor(Color.TRANSPARENT);
    }

    @Override
    public int getItemCount() {
        return offers.size();
    }

    public class MyViewHolder extends RecyclerView.ViewHolder implements View.OnClickListener {

        TextView nameView, titleView, orderView;
        RelativeLayout rowView;

        public MyViewHolder(@NonNull View itemView) {
            super(itemView);
            nameView = itemView.findViewById(R.id.name);
            titleView = itemView.findViewById(R.id.title);
            orderView = itemView.findViewById(R.id.order);
            rowView = itemView.findViewById(R.id.row);
            itemView.setOnClickListener(this);
        }

        @Override
        public void onClick(View itemView) {
            int i = getAdapterPosition();
            if (selectedItems.contains(i)) {
                selectedItems.remove(Integer.valueOf(i));
                rowView.setBackgroundColor(Color.TRANSPARENT);
            } else {
                selectedItems.add(i);
                rowView.setBackgroundColor(Color.GRAY);
            }
        }
    }
}