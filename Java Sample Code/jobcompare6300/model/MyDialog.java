package edu.gatech.seclass.jobcompare6300.model;

import android.app.AlertDialog;
import android.content.Context;
import android.content.DialogInterface;
import android.util.Log;
import android.view.Gravity;
import android.widget.TextView;

import edu.gatech.seclass.jobcompare6300.R;

public class MyDialog {

    public static void showDialogNotice(Context context, String str) {
        AlertDialog.Builder builder = new AlertDialog.Builder(context);

        TextView title = new TextView(context);
        title.setText(R.string.notice);
        title.setGravity(Gravity.CENTER);
        title.setTextSize(24);
        title.setPadding(0,10,0,10);
        builder.setCustomTitle(title);

        builder.setMessage(str);
        builder.setPositiveButton(context.getString(R.string.ok), new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialog, int which) {
                dialog.dismiss();
            }
        });

        builder.show();
    }

}
