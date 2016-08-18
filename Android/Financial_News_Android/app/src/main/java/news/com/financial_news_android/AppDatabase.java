package news.com.financial_news_android;

import com.raizlabs.android.dbflow.annotation.Database;

/**
 * A class defining database name and version
 *
 * Created by Ping He
 */
@Database(name = AppDatabase.NAME, version = AppDatabase.VERSION)
public class AppDatabase {
    // Database name
    public static final String NAME = "AppDatabase";

    // Database version number
    public static final int VERSION = 2;
}
