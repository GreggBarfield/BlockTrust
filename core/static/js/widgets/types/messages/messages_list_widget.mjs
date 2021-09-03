import { Widget } from '../../widget.mjs';
import { Table } from '../../../core/table.mjs';
import { InfoModal } from '../../../core/info_modal.mjs';
import { formatDateTime } from '../../../core/time.mjs';
import { promptNewMessage } from '../../../sales_groups/messages.mjs';
import { promptAccountsAndNewMessage } from './select_and_send_message_to_account.mjs';

export class MessagesListWidget extends Widget {
    constructor(frame) {
        super(frame);
    }

    initType() {
        this.getData("get_account_messages", {}).then((data)=>{
            this.displayMessages(data["messages"]);
        });

        this.onSomeDataLoaded(function () {
            this.frame.innerHTML = "";
            let accounts;
            this.getData("get_accounts_list", {}).then((data)=>{
                accounts=data.accounts;
            });
            let sendMessage = document.createElement("button");
            sendMessage.className = "btn btn-sm btn-primary float-right";
            sendMessage.textContent = "Send Message";
            this.frame.append(sendMessage);
            sendMessage.addEventListener("click", ()=>{
                promptAccountsAndNewMessage(accounts);
            });
        });

        if (this.frame.hasAttribute("data-widget-messages-open")) {
            this.openMessage = parseInt(this.frame.getAttribute("data-widget-messages-open"));
        }
        else {
            this.openMessage = null;
        }

    }

    _openMessage(message) {
        let modal = new InfoModal(
            "Message from " + message.from_name,
            message.data
        );
        modal.getBody().style.whiteSpace = "pre-wrap";
        modal.getBody().style.overflowWrap = "break-word";
    }

    displayMessages(messages) {
        let table = new Table();
        table.attach(this.frame);

        table.setHeader(["Context", "Message", ""]);

        let openedAnyMessage = false;

        if (messages.length == 0) {
            let empty = document.createElement("div");
            empty.style.textAlign = "center";
            empty.textContent = "No Messages";
            this.frame.append(empty);
        }
        else {
            for (const message of messages) {
                let messageShort = message.data;
                if (messageShort.length > 50) {
                    messageShort = messageShort.substring(0, 50) + "...";
                }
                let messageDisplay = document.createElement("div");
                messageDisplay.style.whiteSpace = "pre-wrap";
                messageDisplay.textContent = messageShort;

                let options = document.createElement("div");

                let optionOpen = document.createElement("button");
                optionOpen.className = "btn btn-sm btn-primary";
                optionOpen.textContent = "Open";
                options.append(optionOpen);

                optionOpen.addEventListener("click", ()=>{
                    this._openMessage(message);
                });

                let optionReply = document.createElement("button");
                optionReply.className = "btn btn-sm btn-primary";
                optionReply.textContent = "Reply";
                options.append(optionReply);

                optionReply.addEventListener("click", ()=>{
                    promptNewMessage(message.from_account, message.from_name);
                });

                let context = document.createElement("div");
                let pfrom = document.createElement("div");
                pfrom.textContent = message.from_name + " to " + message.to_name;
                context.append(pfrom);
                let pat = document.createElement("div");
                pat.className = "text-muted";
                pat.textContent = formatDateTime(message.time_sent);
                context.append(pat);

                message.from_name,
                    message.to_name,
                    formatDateTime(message.time_sent)

                table.addRow([
                    context,
                    messageDisplay,
                    options,
                ]);

                if (message["id"] === this.openMessage) {
                    this._openMessage(message);
                    openedAnyMessage = true;
                }
            }
        }

        if (!openedAnyMessage && this.openMessage !== null) {
            new InfoModal(
                "Message Not Found",
                "Sorry, the message requested was not found on this account."
            );
        }
    }
}
