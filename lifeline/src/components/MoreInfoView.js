// author: @dudash
// license: Apache 2.0
import React from "react";
import { observer } from "mobx-react";

function MoreInfoView({ stateStore }) {    
    return (
        <div className="App-homepage-moreinfo">
            Please provide any additional information below
        </div>
    );
}
export default observer(MoreInfoView);