package news.com.financial_news_android;

import android.app.Activity;

import android.app.ActionBar;
import android.app.Fragment;
import android.app.FragmentManager;
import android.content.ContentValues;
import android.content.Context;
import android.content.Intent;
import android.database.DataSetObserver;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.os.Environment;
import android.os.Handler;
import android.os.Message;
import android.support.v4.widget.SwipeRefreshLayout;
import android.util.*;
import android.util.Base64;
import android.view.Gravity;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.support.v4.widget.DrawerLayout;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.ImageView;
import android.widget.ListAdapter;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;

import com.google.android.gms.appindexing.Action;
import com.google.android.gms.appindexing.AppIndex;
import com.google.android.gms.common.api.GoogleApiClient;

import com.loopj.android.http.*;
import com.nostra13.universalimageloader.core.ImageLoader;
import com.nostra13.universalimageloader.core.ImageLoaderConfiguration;
import com.nostra13.universalimageloader.core.assist.FailReason;
import com.nostra13.universalimageloader.core.listener.ImageLoadingListener;
import com.raizlabs.android.dbflow.annotation.Database;
import com.raizlabs.android.dbflow.config.FlowManager;
import com.raizlabs.android.dbflow.sql.language.ConditionGroup;
import com.raizlabs.android.dbflow.sql.language.From;
import com.raizlabs.android.dbflow.sql.language.Method;
import com.raizlabs.android.dbflow.sql.language.SQLite;
import com.raizlabs.android.dbflow.sql.language.property.IProperty;
import com.raizlabs.android.dbflow.structure.BaseModel;
import com.raizlabs.android.dbflow.structure.database.DatabaseWrapper;
import com.raizlabs.android.dbflow.structure.database.transaction.FastStoreModelTransaction;
import com.raizlabs.android.dbflow.structure.database.transaction.ProcessModelTransaction;
import com.raizlabs.android.dbflow.structure.database.transaction.Transaction;

import net.sqlcipher.Cursor;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.lang.reflect.Array;
import java.text.DateFormat;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;
import java.util.List;

import cz.msebera.android.httpclient.Header;

public class MainActivity extends Activity
        implements NavigationDrawerFragment.NavigationDrawerCallbacks {

    /**
     * Fragment managing the behaviors, interactions and presentation of the navigation drawer.
     */
    private NavigationDrawerFragment mNavigationDrawerFragment;

    /**
     * Used to store the last screen title. For use in {@link #restoreActionBar()}.
     */
    private CharSequence mTitle;
    /**
     * ATTENTION: This was auto-generated to implement the App Indexing API.
     * See https://g.co/AppIndexing/AndroidStudio for more information.
     */
    private GoogleApiClient client;

    private SwipeRefreshLayout swipeContainer;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        mNavigationDrawerFragment = (NavigationDrawerFragment)
                getFragmentManager().findFragmentById(R.id.navigation_drawer);
        mTitle = getTitle();

        // Set up the drawer.
        //mNavigationDrawerFragment.setUp(
        //        R.id.navigation_drawer,
        //(DrawerLayout) findViewById(R.id.drawer_layout));
        // ATTENTION: This was auto-generated to implement the App Indexing API.
        // See https://g.co/AppIndexing/AndroidStudio for more information.
        client = new GoogleApiClient.Builder(this).addApi(AppIndex.API).build();

        handler.sendEmptyMessageDelayed(0, 3000);

    }

    Handler handler = new Handler() {
        @Override
        public void handleMessage(Message msg) {
            super.handleMessage(msg);
            findViewById(R.id.loading).setVisibility(View.GONE);
        }
    };

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);

        mNavigationDrawerFragment.onActivityResult(requestCode, resultCode, data);
    }

    @Override
    public void onNavigationDrawerItemSelected(int position) {
        // update the main content by replacing fragments
        FragmentManager fragmentManager = getFragmentManager();
        fragmentManager.beginTransaction()
                .replace(R.id.container, PlaceholderFragment.newInstance(position + 1))
                .commit();
    }

    public void onSectionAttached(int number) {
        switch (number) {
            case 1:
                mTitle = getString(R.string.title_section1);
                break;
            case 2:
                mTitle = getString(R.string.title_section2);
                break;
            case 3:
                mTitle = getString(R.string.title_section3);
                break;
        }
    }

    public void restoreActionBar() {
        ActionBar actionBar = getActionBar();
        actionBar.setNavigationMode(ActionBar.NAVIGATION_MODE_STANDARD);
        actionBar.setDisplayShowTitleEnabled(true);
        actionBar.setTitle(mTitle);
    }

    @Override
    public void onStart() {
        super.onStart();

        // ATTENTION: This was auto-generated to implement the App Indexing API.
        // See https://g.co/AppIndexing/AndroidStudio for more information.
        client.connect();
        Action viewAction = Action.newAction(
                Action.TYPE_VIEW, // TODO: choose an action type.
                "Main Page", // TODO: Define a title for the content shown.
                // TODO: If you have web page content that matches this app activity's content,
                // make sure this auto-generated web page URL is correct.
                // Otherwise, set the URL to null.
                Uri.parse("http://host/path"),
                // TODO: Make sure this auto-generated app URL is correct.
                Uri.parse("android-app://news.com.financial_news_android/http/host/path")
        );
        AppIndex.AppIndexApi.start(client, viewAction);
    }

    @Override
    public void onStop() {
        super.onStop();

        // ATTENTION: This was auto-generated to implement the App Indexing API.
        // See https://g.co/AppIndexing/AndroidStudio for more information.
        Action viewAction = Action.newAction(
                Action.TYPE_VIEW, // TODO: choose an action type.
                "Main Page", // TODO: Define a title for the content shown.
                // TODO: If you have web page content that matches this app activity's content,
                // make sure this auto-generated web page URL is correct.
                // Otherwise, set the URL to null.
                Uri.parse("http://host/path"),
                // TODO: Make sure this auto-generated app URL is correct.
                Uri.parse("android-app://news.com.financial_news_android/http/host/path")
        );
        AppIndex.AppIndexApi.end(client, viewAction);
        client.disconnect();
    }

    /**
     * A placeholder fragment containing a simple view.
     */
    public static class PlaceholderFragment extends Fragment {
        /**
         * The fragment argument representing the section number for this
         * fragment.
         */
        private static final String ARG_SECTION_NUMBER = "section_number";

        public PlaceholderFragment() {
        }

        /**
         * Returns a new instance of this fragment for the given section
         * number.
         */
        public static PlaceholderFragment newInstance(int sectionNumber) {
            PlaceholderFragment fragment = new PlaceholderFragment();
            Bundle args = new Bundle();
            args.putInt(ARG_SECTION_NUMBER, sectionNumber);
            fragment.setArguments(args);
            return fragment;
        }

        List<Article> articles = null;
        ListView lv = null;
        private SwipeRefreshLayout swipeContainer;

        Handler h = new Handler() {
            @Override
            public void handleMessage(Message msg) {
                super.handleMessage(msg);

                articles.addAll(0, (ArrayList<Article>) msg.obj);
                lv.setAdapter(new UsersAdapter(getActivity(), articles));

            }
        };

        String time3;
        public void refresh(){
            swipeContainer.setRefreshing(true);

            SimpleDateFormat df = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
            Calendar cal = Calendar.getInstance();
            cal.add(Calendar.DATE, -5);
            String requestDatetime = df.format(cal.getTime());
            String[] s = requestDatetime.split(" ");
            requestDatetime = s[0] + "T" + s[1] + "Z";

            Calendar cal3 = Calendar.getInstance();
            cal3.add(Calendar.DATE, -3);
            time3 = df.format(cal3.getTime());
            String[] s3 = time3.split(" ");
            time3 = s3[0] + "T" + s3[1] + "Z";

            SQLite.delete(Article.class).where(Article_Table.datetime.lessThanOrEq(requestDatetime))
                    .and(Article_Table.isFav.isNot("1")).execute();
            articles = SQLite.select().from(Article.class).where(Article_Table.source.is("BBC")).and(Article_Table.datetime.greaterThanOrEq(time3)).orderBy(Article_Table.datetime, false).queryList();

            if (articles != null && articles.size() > 0) {
                if (lv.getAdapter() == null || lv.getAdapter().getCount() == 0) {
                    lv.setAdapter(new UsersAdapter(getActivity(), articles));}
                android.database.Cursor aa = SQLite.select(Method.max(Article_Table.datetime)).from(Article.class).query();
                aa.moveToFirst();
                String max = aa.getString(0);

                requestDatetime = requestDatetime.compareTo(max) < 0 ? max : requestDatetime;



                //Toast.makeText(getActivity(), aa.getString(0), Toast.LENGTH_LONG).show();
            }
            //else {
            AsyncHttpClient c = new AsyncHttpClient();

            RequestParams rp = new RequestParams();
            rp.add("format", "json");
            rp.add("latestDatetime", requestDatetime);

            c.get("http://137.43.93.133:8000/articles/article_api_list/", rp, new JsonHttpResponseHandler() {
                @Override
                public void onSuccess(int statusCode, Header[] headers, JSONArray response) {
                    super.onSuccess(statusCode, headers, response);

                    int size = response.length();
                    ArrayList<Article> articles = new ArrayList<Article>();
                    ArrayList<Article> bbc = new ArrayList<Article>();
                    JSONObject obj;
                    Article art;
                    for (int i = 0; i < size; i++) {
                        art = new Article();

                        try {
                            obj = response.getJSONObject(i);
                            art.setContent(obj.getString("Content"));
                            art.setDatetime(obj.getString("DateTime"));
                            art.setHeadline(obj.getString("Headline"));
                            art.setSubHeadline(obj.getString("SubHeadline"));
                            art.setUrl(obj.getString("Url"));
                            art.setKeywords(obj.getString("Keywords"));
                            art.setType(obj.getString("Type"));
                            art.setSource(obj.getString("Source"));
                            art.setImage(obj.getString("Image"));
                            art.setArticleid(obj.getInt("id"));

                            articles.add(art);

                            if ("BBC".equals(art.getSource()) && art.getDatetime().compareTo(time3) >= 0) {
                                bbc.add(art);
                            }

                        } catch (JSONException e) {
                            e.printStackTrace();
                        }
                    }

                    if (articles.size() > 0) {
                    FastStoreModelTransaction.insertBuilder(FlowManager.getModelAdapter(Article.class))
                            .addAll(articles).build().execute(FlowManager.getDatabase(AppDatabase.class).getWritableDatabase());}

                    if (bbc.size() > 0) {h.sendMessage(Message.obtain(h,1,bbc));}
                }


                @Override
                public void onFailure(int statusCode, Header[] headers, String responseString, Throwable throwable) {
                    super.onFailure(statusCode, headers, responseString, throwable);
                }
            });

            swipeContainer.setRefreshing(false);
        }

        @Override
        public View onCreateView(LayoutInflater inflater, ViewGroup container,
                                 Bundle savedInstanceState) {
            View rootView = inflater.inflate(R.layout.fragment_main, container, false);

            lv = (ListView) rootView.findViewById(R.id.listView);

            swipeContainer = (SwipeRefreshLayout) rootView.findViewById(R.id.swipeContainer);

            lv.setOnItemClickListener(new AdapterView.OnItemClickListener() {
                @Override
                public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
                    Intent i = new Intent(parent.getContext(), NewsActivity.class);
                    i.putExtra("article", articles.get(position));
                    parent.getContext().startActivity(i);
                }
            });

            refresh();


            // Setup refresh listener which triggers new data loading
            swipeContainer.setOnRefreshListener(new SwipeRefreshLayout.OnRefreshListener() {
                @Override
                public void onRefresh() {
                    // Your code to refresh the list here.
                    // Make sure you call swipeContainer.setRefreshing(false)
                    // once the network request has completed successfully.
                    refresh();
                }
            });
            // Configure the refreshing colors
            swipeContainer.setColorSchemeResources(android.R.color.holo_blue_bright,
                    android.R.color.holo_green_light,
                    android.R.color.holo_orange_light,
                    android.R.color.holo_red_light);

            //}




            return rootView;
        }

        public class UsersAdapter extends ArrayAdapter<Article> {
            public UsersAdapter(Context context, List<Article> users) {
                super(context, 0, users);
            }

            @Override
            public View getView(final int position, View convertView, ViewGroup parent) {
                View v = convertView;

                if (v == null) {
                    v = LayoutInflater.from(getActivity()).inflate(R.layout.listview_item_main, null);
                }

                Article art = getItem(position);
                ((TextView)v.findViewById(R.id.textView2)).setText(art.getHeadline());
                String time = art.getDatetime().split("T")[0];
                ((TextView)v.findViewById(R.id.textView3)).setText(time);

                final ImageView iv = ((ImageView)v.findViewById(R.id.imageView2));
                iv.setTag(art);

                if (art.getImage() != null && !"".equals(art.getImage())) {

                    File file = imageExsit(Base64.encodeToString(art.getImage().getBytes(), Base64.DEFAULT) + ".jpg");
                    //ImageLoader.getInstance().displayImage(Uri.fromFile(file).toString(), iv);
                    if (file != null)
                        try {
                            //iv.setImageBitmap(BitmapFactory.decodeStream(new FileInputStream(file)));
                            String u = Uri.fromFile(file).toString();
                            ImageLoader.getInstance().displayImage(Uri.decode(u), iv);
                        } catch (Exception e) {
                            setDefaultPic(iv);
                        }
                    else {
                        setDefaultPic(iv);

                        //Bitmap b = ImageLoader.getInstance().loadImageSync(art.getImage());
                        ImageLoader.getInstance().displayImage(art.getImage(), iv, new ImageLoadingListener() {
                            @Override
                            public void onLoadingStarted(String imageUri, View view) {

                            }

                            @Override
                            public void onLoadingFailed(String imageUri, View view, FailReason failReason) {

                            }

                            @Override
                            public void onLoadingComplete(String imageUri, View view, Bitmap loadedImage) {
                                saveImage(loadedImage,
                                        Base64.encodeToString(imageUri.getBytes(), Base64.DEFAULT) + ".jpg");
                            }

                            @Override
                            public void onLoadingCancelled(String imageUri, View view) {

                            }
                        });
                    }


                } else {
                    setDefaultPic(iv);
                }

                return v;
            }
        }

        public void setDefaultPic(ImageView iv) {
            Article art = (Article) iv.getTag();
            String source = art.getSource();

            if ("The New York Times".equals(art.getSource())) {
                iv.setImageResource(R.drawable.nytime);
            }else if ("BBC".equals(art.getSource())) {
                iv.setImageResource(R.drawable.bbc);
            }else if ("ChinaDaily".equals(art.getSource())) {
                iv.setImageResource(R.drawable.chinadaily);
            }else if ("Reuters".equals(art.getSource())) {
                iv.setImageResource(R.drawable.reuters);
            }else {
                iv.setImageResource(R.drawable.sample);
            }


        }

        public File imageExsit(String fname) {
            String root = Environment.getExternalStorageDirectory().toString();
            File myDir = new File(root + "/financial_eye");
            if (!myDir.exists()) {
                myDir.mkdirs();
            }

            File file = new File(myDir, fname);
            if (file.exists()) {
                if (file.length() == 0) {
                    file.delete();
                    return null;
                }
                return file;
            }

            return null;
        }

        public String saveImage(Bitmap finalBitmap, String fname) {

            String root = Environment.getExternalStorageDirectory().toString();
            File myDir = new File(root + "/financial_eye");
            if (!myDir.exists()) {
                myDir.mkdirs();
            }

            File file = new File(myDir, fname);
            if (file.exists())
                return file.getAbsolutePath();

            try {
                FileOutputStream out = new FileOutputStream(file);
                finalBitmap.compress(Bitmap.CompressFormat.JPEG, 90, out);
                out.flush();
                out.close();

            } catch (Exception e) {
                return "";
            }

            return file.getAbsolutePath();
        }

        @Override
        public void onAttach(Activity activity) {
            super.onAttach(activity);
            ((MainActivity) activity).onSectionAttached(
                    getArguments().getInt(ARG_SECTION_NUMBER));
        }
    }

}
