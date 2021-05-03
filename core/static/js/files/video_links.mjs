import {uploadFile} from "./files.mjs";
import {Table} from "../core/table.mjs";
import {InfoModal} from "../core/info_modal.mjs";
export class VideoSession{
    constructor(restrictions={}, attach_node=null, linkIDs=null, linkAuths=null) {
        let that = this;
        this.links = [];
        this.restrictions = restrictions;
        this.linkAuths = linkAuths;

        if (linkIDs !== null) {
            for (const linkID of linkIDs) {
                let link_obj = {
                    
                    "platform": linkID[0],
                   
                    "embed":linkID[1],
                    "uploaded": false,
                    "removed":false
                    
                };
                if (linkID in linkAuths) {
                    link_obj["link"] = linkAuths[linkID]["link"];
                }
                this.links.push(link_obj);
            }
        }

        this.attached = false;

        this.linkBox = document.createElement("div");

        this.table = new Table();
        this.table.attach(this.linkBox);

        this.table.setHeader(["Platform", "Link", "Options"]);
        
        this.updateTable();
        this.addURLButton = document.createElement("button");
        this.addURLButton.className = "btn btn-sm btn-primary";
        this.addURLButton.textContent = "Add Youtube/Vimeo link"
        this.addURLButton.type = "button";
        this.addURLButton.addEventListener("click", ()=> {
           
            this.promptURLBox(this.links);

        });

        this.linkBox.append(this.addURLButton);

        if (attach_node !== null) {
            this.attach(attach_node);
        }

    }
    getLinks() {
        // Gets all uploaded and not removed file IDs
        let result = [];
        console.log(this.links)
        for (const link of this.links) {
            console.log(link["removed"]);

            if (link["removed"])
                continue;
          
            result.push([link["platform"],link["embed"]]);
        }
        return result;
    }
    attach(attach_node) {
        this.attached = true;
        this.frame = attach_node;
        this.frame.append(this.linkBox);
    }
    remove(link) {
        // if ("removed" in link) {
            link["removed"] = !link["removed"];
        // }
        // else {
        //     link["removed"] = true;
        // }
        return link["removed"];
    }
    updateTable() {
        for (let link of this.links) {
            let linkID = link.platform;
            if ("platform" in link && link.uploaded == true) {
                linkID = link.platform;
            }
            let linkName = "";
            if ("embed" in link) {
                linkName = link.embed;
            }
            if (!("row" in link)) {
                
                let optionsDiv = document.createElement("div");
                
                let removeButton = document.createElement("button");
                removeButton.textContent = "Remove";
                removeButton.className = "btn btn-sm btn-danger";
                removeButton.type = "button";
                removeButton.addEventListener("click", ()=>{
                    if (this.remove(link)) {
                        removeButton.textContent = "Add";
                    }
                    else {
                        removeButton.textContent = "Remove";
                    }
                    this.updateTable();
                });
                optionsDiv.append(removeButton);
                
                link["row"] = this.table.addRow([linkID, linkName, optionsDiv]);
            }
            this.table.setValue(link["row"], 0, linkID);
            this.table.setValue(link["row"], 1, linkName);

            if (link["removed"]) {
                link["row"].style.textDecoration = "line-through";
            }
            else {
                link["row"].style.textDecoration = "initial";
            }
        }
    }
    
    promptURLBox(files){
        let infoModal = new InfoModal("Adding video link(s) ");
        let modalBody = infoModal.getBody();

        let form = document.createElement("form");
        modalBody.append(form);

        let formGroup = document.createElement("div");
        formGroup.className = "form-group";
        form.append(formGroup);

        let label = document.createElement("label");
        label.textContent = "Use , to separate links";
        formGroup.append(label);

        let textArea = document.createElement("textarea");
        textArea.className = "form-control";
        textArea.setAttribute("maxlength", 1000);
        formGroup.append(textArea);

        let submitButton = document.createElement("button");
        submitButton.textContent = "Submit";
        submitButton.className = "btn btn-primary";
        infoModal.getFooter().append(submitButton);

        submitButton.addEventListener("click", ()=>{
            handleUrlInput(textArea.value);
            infoModal.close();
            this.updateTable();
        
        });
        //allow to multiple links
        function parseYouTubeTokenByUri(url){
            var regExp = /^.*((youtu.be\/)|(v\/)|(\/u\/\w\/)|(embed\/)|(watch\?))\??v?=?([^#&?]*).*/;
            var match = url.match(regExp);
            return (match&&match[7].length==11)? match[7] : false;
        }
        function parseVimeoTokenByUri(url){
            var regExp = /^.*(vimeo\.com\/)((channels\/[A-z]+\/)|(groups\/[A-z]+\/videos\/))?([0-9]+)/
            var match = url.match(regExp);
            return match[5]
        }
        function handleUrlInput(links){
            var urls= links.split(",");
            // console.log(urls);
            var tag=null
            var platform="N/A";
            var id="";
            for( const url of urls){
                if(url.includes("youtube") || url.includes("vimeo")){
                    tag = url.split("/");
               
                    if(tag[2].includes("youtube")){
                        platform="youtube";
                        id=parseYouTubeTokenByUri(url);
                    }
                    else{
                        platform="vimeo";
                        id=parseVimeoTokenByUri(url);
            
                    }
                    let file_obj = {
                        "platform": platform,
                        "embed":id,
                        "uploaded": false,
                        "removed":false
                    };
                    files.push(file_obj);
                    console.log(files);
                }
               
            }

        }
        
    }
   
}