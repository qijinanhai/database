from multipage import MultiPage
import pages.Home as home
import pages.seller1 as seller
import pages.user as user
import pages.order_detail as order_detail

app = MultiPage()
app.add_page('Home', home.app)
app.add_page('seller', seller.app)
app.add_page('user', user.app)
app.add_page('order_detail', order_detail.app)

if __name__ == '__main__':
    app.run()
