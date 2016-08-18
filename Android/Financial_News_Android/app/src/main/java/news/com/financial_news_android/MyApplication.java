package news.com.financial_news_android;

import android.app.Application;

import com.nostra13.universalimageloader.core.ImageLoader;
import com.nostra13.universalimageloader.core.ImageLoaderConfiguration;
import com.raizlabs.android.dbflow.config.FlowConfig;
import com.raizlabs.android.dbflow.config.FlowManager;

/**
 * One App only has one Application class which init some library
 *
 * Created by Ping He
 */
public class MyApplication extends Application {

    @Override
    public void onCreate() {
        super.onCreate();

        // init FlowManager
        FlowManager.init(new FlowConfig.Builder(this).build());

        // init ImageLoader
        ImageLoaderConfiguration c = new ImageLoaderConfiguration.Builder(this).build();
        ImageLoader.getInstance().init(c);

    }
}
