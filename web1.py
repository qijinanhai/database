from multipage import MultiPage
import pages.Home as home
import pages.seller1 as seller

app = MultiPage()
app.add_page('Home',home.app)
app.add_page('seller',seller.app)
# app.add_app('user',None)

if __name__=='__main__':
    app.run()
