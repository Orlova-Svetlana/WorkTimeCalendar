import {Form} from "react-bootstrap";
import React from "react";

const Select = ({data, fetching, onChange, selectedId, formLabel='', placeholder = '', keyName = 'id', titleName = 'name'}) => {
    return <React.Fragment>
        {formLabel.length > 0 && <Form.Label>{formLabel}:</Form.Label>}
        <Form.Select disabled={fetching} onChange={onChange} value={selectedId}>
            <option value={0}>{data.length > 0 ? placeholder : ''}</option>
            {data.map(item=>{
                return <option key={`key_${item[keyName]}`} value={item[keyName]}>{item[titleName]}</option>
            })}
        </Form.Select>
    </React.Fragment>
};

export default Select;