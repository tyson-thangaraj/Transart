package news.com.financial_news_android;

import com.raizlabs.android.dbflow.annotation.Database;

/**
 * Created by ping on 2016/6/30.
 */
@Database(name = AppDatabase.NAME, version = AppDatabase.VERSION)
public class AppDatabase {
    public static final String NAME = "AppDatabase";

    public static final int VERSION = 2;
}
