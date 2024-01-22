import { Widget } from '../../widget.mjs';

export class MarketPlaceWidget extends Widget {
    constructor(frame) {
        super(frame);
    }

    initType = async() => {
        let seedstockProducers = JSON.parse(this.frame.getAttribute("data-widget-seedstock-producers"));
        this.frame.innerHTML = "";
        let seedstockProducersContainer = this.makeSeedstockProducersContainer(seedstockProducers);
        this.frame.append(seedstockProducersContainer);
    }

    makeSeedstockProducersContainer = () =>{
        
    }
}