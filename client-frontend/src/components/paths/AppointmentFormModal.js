import {Alert, Button, Form, Modal} from "react-bootstrap";
import React, {useState} from "react";
import axios from "axios";
import {API_ADDRESS} from "../../constants";

const AppointmentFormModal = ({selectedScheduleId, selectedScheduleDate, selectedSegment, procedureId, procedureName, onClose, onSuccess}) => {

    const [clientFio, setClientFio] = useState('Client 1');
    const [clientEmail, setClientEmail] = useState('client1@email.com');
    const [clientPhone, setClientPhone] = useState('1234567890');
    const [formErrors, setFormErrors] = useState([]);

    const onSave = () => {
        const formData = new FormData(document.getElementById('new_appointment_form'));
        setFormErrors([]);
        axios.post(`${API_ADDRESS}appointments/`, formData)
            .then(data=>{
                onSuccess()
            })
            .catch(data=>{
                if (data?.response?.data) {
                    setFormErrors(data.response.data)
                }
            });
    };

    return <Modal show={true} onHide={onClose} >
        <Modal.Header closeButton>
            <Modal.Title>Запись на приём</Modal.Title>
        </Modal.Header>
        <Modal.Body>
            <Form id="new_appointment_form">
                {formErrors?.non_field_errors && formErrors.non_field_errors.map((nfe, index)=>{
                    return <Alert key={`nfe_${index}`} variant={'danger'}>{nfe}</Alert>
                })}
                <Form.Group className="mb-3">
                    <Form.Label>Date</Form.Label>
                    <Form.Control name="schedule" type="hidden" value={selectedScheduleId}/>
                    <Form.Control type="text" readOnly={true} value={selectedScheduleDate}/>
                </Form.Group>
                <Form.Group className="mb-3">
                    <Form.Label>Segment</Form.Label>
                    <Form.Control name="appointment_time" type="text" readOnly={true} value={selectedSegment}/>
                </Form.Group>
                <Form.Group className="mb-3">
                    <Form.Label>Procedure</Form.Label>
                    <Form.Control name="procedure" type="hidden" value={procedureId}/>
                    <Form.Control type="text" readOnly={true} value={procedureName}/>
                </Form.Group>
                <Form.Group className="mb-3">
                    <Form.Label>Ф.И.О</Form.Label>
                    <Form.Control type="text" name="client_name" className={formErrors?.client_name ? 'is-invalid' : ''} value={clientFio} onChange={(event)=>setClientFio(event.target.value)}/>
                    {formErrors?.client_name && <div className={'invalid-feedback'}>{formErrors?.client_name}</div>}
                </Form.Group>
                <Form.Group className="mb-3">
                    <Form.Label>Email</Form.Label>
                    <Form.Control type="email" name="client_email" className={formErrors?.client_email ? 'is-invalid' : ''} value={clientEmail} onChange={(event)=>setClientEmail(event.target.value)}/>
                    {formErrors?.client_email && <div className={'invalid-feedback'}>{formErrors?.client_name}</div>}
                </Form.Group>
                <Form.Group className="mb-3">
                    <Form.Label>Телефон</Form.Label>
                    <Form.Control type="text" name="client_phone" className={formErrors?.client_phone ? 'is-invalid' : ''} value={clientPhone} onChange={(event)=>setClientPhone(event.target.value)}/>
                    {formErrors?.client_phone && <div className={'invalid-feedback'}>{formErrors?.client_name}</div>}
                </Form.Group>
            </Form>
        </Modal.Body>
        <Modal.Footer>
            <Button variant="secondary" onClick={onClose}>Close</Button>
            <Button variant="primary" onClick={onSave}>Save Changes</Button>
        </Modal.Footer>
    </Modal>
};

export default AppointmentFormModal;