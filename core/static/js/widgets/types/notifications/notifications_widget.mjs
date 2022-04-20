import { Widget } from '../../widget.mjs';

export class NotificationsWidget extends Widget {
    constructor(frame){
        super(frame);
    }

    initType(){
        this.getData(
            "get_notifications_for_user"
        ).then((data) => {
            this.data = data;
            this.makeNotificationsAlert();
        });

        this.onSomeDataLoaded(function () {
            this.frame.innerHTML = "";
        });
    }

    makeNotificationsAlert(){

        function createLink(linkRoute, linkText){
            let link = document.createElement('a')
            link.href = linkRoute;
            link.innerHTML = linkText;
            return link;
        }

        this.alert = document.createElement('div');
        this.alert.className = "alert alert-success alert-dismissible fade show p-1";
        this.alert.setAttribute("role", "alert");

        let closeButton = document.createElement('button');
        closeButton.type = "button";
        closeButton.className = "close";
        closeButton.innerHTML = "&times;";
        closeButton.setAttribute("data-dismiss", "alert");
        closeButton.setAttribute("aria-label", "Close");
        this.alert.append(closeButton);
        let message = document.createElement('p');
        message.className = "mt-2";
        if(this.data.unread_notifications_count>0 && this.data.pending_connection_requests_count>0){
            message.textContent = "You have ";
            let unreadNotificationslink = createLink("/dashboard/notifications", this.data.unread_notifications_count.toString() + " unread notification(s)");
            message.append(unreadNotificationslink);
            message.append(" and ");
            let pendingRequestsLink = createLink("/dashboard/view-invites", this.data.pending_connection_requests_count.toString() + " pending connection request(s)");
            message.append(pendingRequestsLink);
        }
        else if(this.data.unread_notifications_count>0){
            message.textContent = "You have ";
            let unreadNotificationslink = createLink("/dashboard/notifications", this.data.unread_notifications_count.toString() + " unread notification(s)");
            message.append(unreadNotificationslink);
        }
        else if(this.data.pending_connection_requests_count>0){
            message.textContent = "You have ";
            let pendingRequestsLink = createLink("/dashboard/view-invites", this.data.pending_connection_requests_count.toString() + " pending connection request(s)");
            message.append(pendingRequestsLink);
        }
        this.alert.append(message);
        $(this.alert).alert();
        if(this.data.unread_notifications_count>0 || this.data.pending_connection_requests_count>0)
        {
            this.frame.append(this.alert);
        }
    }
}