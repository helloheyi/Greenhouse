package edu.gatech.seclass.jobcompare6300.database;

import android.content.ContentValues;
import android.content.Context;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.provider.BaseColumns;
import android.util.Log;

import java.util.ArrayList;
import java.util.List;

import edu.gatech.seclass.jobcompare6300.DataManager;
import edu.gatech.seclass.jobcompare6300.model.OfferDetail;

public class OfferDetailDAO {

    private DBHelper dbHelper;

    public OfferDetailDAO(Context context) {
        dbHelper = new DBHelper(context);
    }

    public void closeDBHelper() {
        dbHelper.close();
    }

    public void add(OfferDetail offer, boolean isJob) {
        // Gets the data repository in write mode
        SQLiteDatabase database = dbHelper.getWritableDatabase();

        // Create a new map of values, where column names are the keys
        ContentValues values = new ContentValues();

        int intIsJob = (isJob) ? 1 : 0;
        values.put(DBHelper.OffersEntry.COLUMN_NAME_IS_JOB, intIsJob);
        values.put(DBHelper.OffersEntry.COLUMN_NAME_TITLE, offer.getTitle());
        values.put(DBHelper.OffersEntry.COLUMN_NAME_COMPANY_NAME, offer.getName());
        values.put(DBHelper.OffersEntry.COLUMN_NAME_CITY, offer.getLocation().city);
        values.put(DBHelper.OffersEntry.COLUMN_NAME_STATE, offer.getLocation().state);
        values.put(DBHelper.OffersEntry.COLUMN_NAME_COST_OF_LIVING, offer.getLocation().costOfLiving);
        values.put(DBHelper.OffersEntry.COLUMN_NAME_YEARLY_SALARY, offer.getSalary());
        values.put(DBHelper.OffersEntry.COLUMN_NAME_YEARLY_BONUS, offer.getBonus());
        values.put(DBHelper.OffersEntry.COLUMN_NAME_NUMBER_OF_STOCK, offer.getStockOptions());
        values.put(DBHelper.OffersEntry.COLUMN_NAME_HOME_FUND, offer.getBenefits().getHomeProgramFund());
        values.put(DBHelper.OffersEntry.COLUMN_NAME_HOLIDAYS, offer.getBenefits().getHolidays());
        values.put(DBHelper.OffersEntry.COLUMN_NAME_INTERNET_STIPEND, offer.getBenefits().getInternetStipend());

        // Insert the new row, returning the primary key value of the new row
        long newRowId = database.insert(DBHelper.OffersEntry.TABLE_NAME, null, values);

        // Close the database
        database.close();
    }

    public int deleteByFlag(boolean isJob) {
        SQLiteDatabase database = dbHelper.getWritableDatabase();

        // Define 'where' part of query.
        String selection = DBHelper.OffersEntry.COLUMN_NAME_IS_JOB + " = ?";

        // Specify arguments in placeholder order.
        int intIsJob = (isJob) ? 1 : 0;
        String[] selectionArgs = new String[] {String.valueOf(intIsJob)};

        // Issue SQL statement.
        int deletedRows = database.delete(DBHelper.OffersEntry.TABLE_NAME, selection, selectionArgs);

        database.close();

        if (deletedRows == 0) {
            return 0;
        } else {
            return deletedRows;
        }

    }

    public void update(String originTitle, OfferDetail offer, boolean isJob) {
        SQLiteDatabase database = dbHelper.getWritableDatabase();
        ContentValues values = new ContentValues();

        if (isJob == DataManager.DATABASE_JOB) { // Update the current job
            int intIsJob = (isJob) ? 1 : 0;
            values.put(DBHelper.OffersEntry.COLUMN_NAME_IS_JOB, intIsJob);
            values.put(DBHelper.OffersEntry.COLUMN_NAME_TITLE, offer.getTitle());
            values.put(DBHelper.OffersEntry.COLUMN_NAME_COMPANY_NAME, offer.getName());
            values.put(DBHelper.OffersEntry.COLUMN_NAME_CITY, offer.getLocation().city);
            values.put(DBHelper.OffersEntry.COLUMN_NAME_STATE, offer.getLocation().state);
            values.put(DBHelper.OffersEntry.COLUMN_NAME_COST_OF_LIVING, offer.getLocation().costOfLiving);
            values.put(DBHelper.OffersEntry.COLUMN_NAME_YEARLY_SALARY, offer.getSalary());
            values.put(DBHelper.OffersEntry.COLUMN_NAME_YEARLY_BONUS, offer.getBonus());
            values.put(DBHelper.OffersEntry.COLUMN_NAME_NUMBER_OF_STOCK, offer.getStockOptions());
            values.put(DBHelper.OffersEntry.COLUMN_NAME_HOME_FUND, offer.getBenefits().getHomeProgramFund());
            values.put(DBHelper.OffersEntry.COLUMN_NAME_HOLIDAYS, offer.getBenefits().getHolidays());
            values.put(DBHelper.OffersEntry.COLUMN_NAME_INTERNET_STIPEND, offer.getBenefits().getInternetStipend());
        }

        // Which row to update, based on the title
        String selection = DBHelper.OffersEntry.COLUMN_NAME_TITLE + " = ?";
        String[] selectionArgs = new String[] {originTitle};

        int count = database.update(
                DBHelper.OffersEntry.TABLE_NAME,
                values,
                selection,
                selectionArgs);

        database.close();
    }

    public OfferDetail getCurrentJobFromDB() {
        // Gets the data repository in write mode
        SQLiteDatabase database = dbHelper.getWritableDatabase();

        Cursor cursor = database.rawQuery("select * from " + DBHelper.OffersEntry.TABLE_NAME +
                " where " + DBHelper.OffersEntry.COLUMN_NAME_IS_JOB + "=" + DataManager.DATABASE_JOB, null);

        int count = cursor.getCount();
        if (count == 0) {
            return null;
        }

        cursor.moveToFirst();

        String title = cursor.getString(cursor.getColumnIndexOrThrow(DBHelper.OffersEntry.COLUMN_NAME_TITLE));
        String name = cursor.getString(cursor.getColumnIndexOrThrow(DBHelper.OffersEntry.COLUMN_NAME_COMPANY_NAME));
        String city = cursor.getString(cursor.getColumnIndexOrThrow(DBHelper.OffersEntry.COLUMN_NAME_CITY));
        String state = cursor.getString(cursor.getColumnIndexOrThrow(DBHelper.OffersEntry.COLUMN_NAME_STATE));
        float costOfLiving = cursor.getFloat(cursor.getColumnIndexOrThrow(DBHelper.OffersEntry.COLUMN_NAME_COST_OF_LIVING));
        float salary = cursor.getFloat(cursor.getColumnIndexOrThrow(DBHelper.OffersEntry.COLUMN_NAME_YEARLY_SALARY));
        float bonus = cursor.getFloat(cursor.getColumnIndexOrThrow(DBHelper.OffersEntry.COLUMN_NAME_YEARLY_BONUS));
        int stock = cursor.getInt(cursor.getColumnIndexOrThrow(DBHelper.OffersEntry.COLUMN_NAME_NUMBER_OF_STOCK));
        float homeFund = cursor.getFloat(cursor.getColumnIndexOrThrow(DBHelper.OffersEntry.COLUMN_NAME_HOME_FUND));
        float holiday = cursor.getFloat(cursor.getColumnIndexOrThrow(DBHelper.OffersEntry.COLUMN_NAME_HOLIDAYS));
        float internet = cursor.getFloat(cursor.getColumnIndexOrThrow(DBHelper.OffersEntry.COLUMN_NAME_INTERNET_STIPEND));

        OfferDetail offer = DataManager.addOffer(title, name, city, state, costOfLiving,
                salary, bonus, stock, homeFund, holiday, internet);

        cursor.close();
        database.close();

        return offer;
    }

    public List<OfferDetail> getOffersList() {
        // Gets the data repository in write mode
        SQLiteDatabase database = dbHelper.getReadableDatabase();

        // Define a projection that specifies which columns from the database
        String[] projection = {
                BaseColumns._ID,
                DBHelper.OffersEntry.COLUMN_NAME_TITLE,
                DBHelper.OffersEntry.COLUMN_NAME_COMPANY_NAME
        };

        Cursor cursor = database.rawQuery("select * from " + DBHelper.OffersEntry.TABLE_NAME +
                " where " + DBHelper.OffersEntry.COLUMN_NAME_IS_JOB + "==" + DataManager.DATABASE_OFFER, null);
        int count = cursor.getCount();

        if (count == 0) {
            return null;
        }

        // Get all rows and store them to the list
        List<OfferDetail> list = new ArrayList<>();
        while(cursor.moveToNext()) {
            long itemId = cursor.getLong(cursor.getColumnIndexOrThrow(DBHelper.OffersEntry._ID));
            String title = cursor.getString(cursor.getColumnIndexOrThrow(DBHelper.OffersEntry.COLUMN_NAME_TITLE));
            String name = cursor.getString(cursor.getColumnIndexOrThrow(DBHelper.OffersEntry.COLUMN_NAME_COMPANY_NAME));
            String city = cursor.getString(cursor.getColumnIndexOrThrow(DBHelper.OffersEntry.COLUMN_NAME_CITY));
            String state = cursor.getString(cursor.getColumnIndexOrThrow(DBHelper.OffersEntry.COLUMN_NAME_STATE));
            float costOfLiving = cursor.getFloat(cursor.getColumnIndexOrThrow(DBHelper.OffersEntry.COLUMN_NAME_COST_OF_LIVING));
            float salary = cursor.getFloat(cursor.getColumnIndexOrThrow(DBHelper.OffersEntry.COLUMN_NAME_YEARLY_SALARY));
            float bonus = cursor.getFloat(cursor.getColumnIndexOrThrow(DBHelper.OffersEntry.COLUMN_NAME_YEARLY_BONUS));
            int stock = cursor.getInt(cursor.getColumnIndexOrThrow(DBHelper.OffersEntry.COLUMN_NAME_NUMBER_OF_STOCK));
            float homeFund = cursor.getFloat(cursor.getColumnIndexOrThrow(DBHelper.OffersEntry.COLUMN_NAME_HOME_FUND));
            float holiday = cursor.getFloat(cursor.getColumnIndexOrThrow(DBHelper.OffersEntry.COLUMN_NAME_HOLIDAYS));
            float internet = cursor.getFloat(cursor.getColumnIndexOrThrow(DBHelper.OffersEntry.COLUMN_NAME_INTERNET_STIPEND));
            OfferDetail offer = DataManager.addOffer(title, name, city, state, costOfLiving,
                    salary, bonus, stock, homeFund, holiday, internet);

            list.add(offer);
        }

        cursor.close();
        database.close();

        return list;
    }
}
