package news.com.financial_news_android;

import android.app.Activity;

import android.app.ActionBar;
import android.app.Fragment;
import android.app.FragmentManager;
import android.content.ContentValues;
import android.content.Context;
import android.content.Intent;
import android.database.DataSetObserver;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.os.Handler;
import android.os.Message;
import android.util.Log;
import android.view.Gravity;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.support.v4.widget.DrawerLayout;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.ListAdapter;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;

import com.google.android.gms.appindexing.Action;
import com.google.android.gms.appindexing.AppIndex;
import com.google.android.gms.common.api.GoogleApiClient;

import com.loopj.android.http.*;
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

import java.lang.reflect.Array;
import java.util.ArrayList;
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

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        mNavigationDrawerFragment = (NavigationDrawerFragment)
                getFragmentManager().findFragmentById(R.id.navigation_drawer);
        mTitle = getTitle();

        // Set up the drawer.
        mNavigationDrawerFragment.setUp(
                R.id.navigation_drawer,
                (DrawerLayout) findViewById(R.id.drawer_layout));
        // ATTENTION: This was auto-generated to implement the App Indexing API.
        // See https://g.co/AppIndexing/AndroidStudio for more information.
        client = new GoogleApiClient.Builder(this).addApi(AppIndex.API).build();


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
        @Override
        public View onCreateView(LayoutInflater inflater, ViewGroup container,
                                 Bundle savedInstanceState) {
            View rootView = inflater.inflate(R.layout.fragment_main, container, false);

            final ListView lv = (ListView) rootView.findViewById(R.id.listView);

            lv.setOnItemClickListener(new AdapterView.OnItemClickListener() {
                @Override
                public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
                    Intent i = new Intent(parent.getContext(), NewsActivity.class);
                    i.putExtra("article", articles.get(position));
                    parent.getContext().startActivity(i);
                }
            });


            final Handler h = new Handler() {
                @Override
                public void handleMessage(Message msg) {
                    super.handleMessage(msg);

                    articles.addAll(0, (ArrayList<Article>) msg.obj);
                    lv.setAdapter(new UsersAdapter(getActivity(), articles));
                    //lv.setAdapter(new UsersAdapter(getActivity(), articles));

                    //articles = SQLite.select().from(Article.class).queryList();
                    //lv.setAdapter(new UsersAdapter(getActivity(), articles));

                    //((TextView) MainActivity.this.findViewById(R.id.tttt)).setText(arts.get(0).getContent());
                }
            };

            articles = SQLite.select().from(Article.class).queryList();

            String requestDatetime = "2016-06-01T00:00:00Z";
            if (articles != null && articles.size() > 0) {
                lv.setAdapter(new UsersAdapter(getActivity(), articles));
                android.database.Cursor aa = SQLite.select(Method.max(Article_Table.datetime)).from(Article.class).query();
                aa.moveToFirst();
                requestDatetime = aa.getString(0);

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
                        Article art;
                        JSONObject obj;
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

                                articles.add(art);
                            } catch (JSONException e) {
                                e.printStackTrace();
                            }
                        }

                        FastStoreModelTransaction.insertBuilder(FlowManager.getModelAdapter(Article.class))
                                .addAll(articles).build().execute(FlowManager.getDatabase(AppDatabase.class).getWritableDatabase());

                    /*ProcessModelTransaction<Article> processModelTransaction =
                            new ProcessModelTransaction.Builder<>(new ProcessModelTransaction.ProcessModel<Article>() {
                                @Override
                                public void processModel(Article model) {
                                    // call some operation on model here
                                    //model.save();
                                    model.insert(); // or
                                    //model.delete(); // or
                                }
                            }).addAll(articles).build();
                    Transaction transaction = FlowManager.getDatabase(AppDatabase.class).beginTransactionAsync(processModelTransaction).build();
                    transaction.execute();*/

                        h.sendMessage(Message.obtain(h,1,articles));
                    }


                    @Override
                    public void onFailure(int statusCode, Header[] headers, String responseString, Throwable throwable) {
                        super.onFailure(statusCode, headers, responseString, throwable);
                    }
                });
            //}




            return rootView;
        }

        public class UsersAdapter extends ArrayAdapter<Article> {
            public UsersAdapter(Context context, List<Article> users) {
                super(context, 0, users);
            }

            @Override
            public View getView(int position, View convertView, ViewGroup parent) {
                View v = convertView;

                if (v == null) {
                    v = LayoutInflater.from(getActivity()).inflate(R.layout.listview_item_main, null);
                }

                ((TextView)v.findViewById(R.id.textView2)).setText(getItem(position).getHeadline());

                return v;
            }
        }

        @Override
        public void onAttach(Activity activity) {
            super.onAttach(activity);
            ((MainActivity) activity).onSectionAttached(
                    getArguments().getInt(ARG_SECTION_NUMBER));
        }
    }

}
