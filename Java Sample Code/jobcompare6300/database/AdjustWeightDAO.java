package edu.gatech.seclass.jobcompare6300.database;

import android.content.ContentValues;
import android.content.Context;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.provider.BaseColumns;

import java.util.ArrayList;
import java.util.List;

import edu.gatech.seclass.jobcompare6300.model.JobWeightSettings;
public class AdjustWeightDAO {
    private DBHelper dbHelper;
    public AdjustWeightDAO(Context context) {
        dbHelper = new DBHelper(context);
    }
    public void addOrUpdateJobWeightSettings(JobWeightSettings settings) {
        SQLiteDatabase db = dbHelper.getWritableDatabase();
        ContentValues values = new ContentValues();
        values.put(DBHelper.JobWeightSettingsEntry.COLUMN_NAME_AYS, settings.getAYS());
        values.put(DBHelper.JobWeightSettingsEntry.COLUMN_NAME_AYB, settings.getAYB());
        values.put(DBHelper.JobWeightSettingsEntry.COLUMN_NAME_CSO, settings.getCSO());
        values.put(DBHelper.JobWeightSettingsEntry.COLUMN_NAME_HBP, settings.getHBP());
        values.put(DBHelper.JobWeightSettingsEntry.COLUMN_NAME_PCH, settings.getPCH());
        values.put(DBHelper.JobWeightSettingsEntry.COLUMN_NAME_MIS, settings.getMIS());

        // Attempt to update the settings if they exist
        int rowsAffected = db.update(DBHelper.JobWeightSettingsEntry.TABLE_NAME, values, null, null);

        // If no rows were updated, insert the new settings
        if (rowsAffected == 0) {
            db.insert(DBHelper.JobWeightSettingsEntry.TABLE_NAME, null, values);
        }
        db.close();
    }
    public JobWeightSettings getJobWeight() {
        SQLiteDatabase db = dbHelper.getReadableDatabase();
        JobWeightSettings settings = new JobWeightSettings(); // Instantiate settings object

        Cursor cursor = db.query(
                DBHelper.JobWeightSettingsEntry.TABLE_NAME, // The table to query
                null, // The columns to return (null returns all columns)
                null, // The columns for the WHERE clause
                null, // The values for the WHERE clause
                null, // Don't group the rows
                null, // Don't filter by row groups
                null  // The sort order
        );

        if (cursor.moveToFirst()) {
            // Populate the settings object with database values if available
            settings.setAYS(cursor.getInt(cursor.getColumnIndexOrThrow(DBHelper.JobWeightSettingsEntry.COLUMN_NAME_AYS)));
            settings.setAYB(cursor.getInt(cursor.getColumnIndexOrThrow(DBHelper.JobWeightSettingsEntry.COLUMN_NAME_AYB)));
            settings.setCSO(cursor.getInt(cursor.getColumnIndexOrThrow(DBHelper.JobWeightSettingsEntry.COLUMN_NAME_CSO)));
            settings.setHBP(cursor.getInt(cursor.getColumnIndexOrThrow(DBHelper.JobWeightSettingsEntry.COLUMN_NAME_HBP)));
            settings.setPCH(cursor.getInt(cursor.getColumnIndexOrThrow(DBHelper.JobWeightSettingsEntry.COLUMN_NAME_PCH)));
            settings.setMIS(cursor.getInt(cursor.getColumnIndexOrThrow(DBHelper.JobWeightSettingsEntry.COLUMN_NAME_MIS)));
        } else {
            // If no rows were returned, set default values of 1 for all settings
            settings.setAYS(1);
            settings.setAYB(1);
            settings.setCSO(1);
            settings.setHBP(1);
            settings.setPCH(1);
            settings.setMIS(1);
        }

        cursor.close(); // Close the cursor
        db.close(); // Close the database

        return settings; // Return the settings object
    }


}
