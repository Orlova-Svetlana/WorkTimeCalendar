import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';
import {Container, Form, Row} from "react-bootstrap";
import axios from "axios";
import {useEffect, useState} from "react";


const API_ADDRESS = 'http://localhost:8000/api/v1/client/';

const App = () => {

    const paths = [
        {index: 'p', label: 'Профессиональный профиль'},
        {index: 's', label: 'Специализация'},
        {index: 'w', label: 'Специалист'},
        {index: 'l', label: 'Локация'},
        {index: 'pr', label: 'Процедура'},
    ];

    const [pathId, setPathId] = useState('');

    useEffect(()=>{

        setProfiles([]);
        setProfileId(0);
        setSpecializations([]);
        setSpecializationId(0);

        switch (pathId) {
            case 'p':
                axios.get(`${API_ADDRESS}professionalprofiles/`).then(response => {
                    setProfiles(response.data);
                });
                break;
            case 's':
                break;
            case 'w':
                break;
            case 'l':
                break;
            case 'pr':
                break;
        }
    }, [pathId]);


    const [profiles, setProfiles] = useState([]);
    const [profileId, setProfileId] = useState(0);

    const [specializations, setSpecializations] = useState([]);
    const [specializationId, setSpecializationId] = useState(0);

    const [workers, setWorkers] = useState([]);
    const [workerId, setWorkerId] = useState(0);

    const [procedures, setProcedures] = useState([]);
    const [procedureId, setProcedureId] = useState(0);

    const [schedules, setSchedules] = useState([]);
    const [appointments, setAppointments] = useState([]);


    useEffect(()=>{
        setWorkers([]);
        setWorkerId(0);
        setProcedures([]);
        setProcedureId(0);

        if (specializationId > 0) {
            const url = `${API_ADDRESS}workers/?specialization=${specializationId}`;
            axios.get(url).then(response => {
                setWorkers(response.data);
            });

            const url2 = `${API_ADDRESS}procedures/?specialization=${specializationId}`;
            axios.get(url2).then(response => {
                setProcedures(response.data);
            });
        }
    }, [specializationId]);

    useEffect(()=>{
        setProfileId(0)
    }, [profiles]);

    useEffect(()=>{
        setSpecializations([]);
        if (profileId > 0) {
            const url = `${API_ADDRESS}specializations/?professional_profile=${profileId}`;
            axios.get(url).then(response => {
                setSpecializations(response.data);
            });
        }
    }, [profileId]);

    useEffect(()=>{
        setSchedules([]);
        if (workerId > 0 && procedureId > 0) {
            axios.get(`${API_ADDRESS}schedules/?worker=${workerId}`).then(response => {
                setSchedules(response.data);
            });
            axios.get(`${API_ADDRESS}appointments/?worker=${workerId}&date=&procedure=${procedureId}`).then(response => {
                setAppointments(response.data);
            });
        }
    }, [workerId, procedureId]);

    useEffect(()=>{
        console.log('appointments', appointments);
        console.log('schedules', schedules);
    }, [appointments, schedules]);

    return <Container>
        <Form>

            <Form.Group as={Row} className="mb-3">
                <Form.Label>Поиск по:</Form.Label>
                <Form.Select onChange={(event)=>{setPathId(event.target.value)}} value={pathId}>
                    <option value=""></option>
                    {paths.map(p=>{
                        return <option key={`path_${p.index}`} value={p.index}>{p.label}</option>
                    })}
                </Form.Select>
            </Form.Group>
            <Form.Group as={Row} className="mb-3">
                <Form.Label>Профессиональный профиль:</Form.Label>
                <Form.Select onChange={(event)=>{setProfileId(event.target.value)}} value={profileId}>
                    <option value={0}>{profiles.length > 0 ? 'выберите профиль' : ''}</option>
                    {profiles.map(profile=>{
                        return <option key={`profile_${profile.id}`} value={profile.id}>{profile.name}</option>
                    })}
                </Form.Select>
            </Form.Group>
            <Form.Group as={Row} className="mb-3">
                <Form.Label>Специализация:</Form.Label>
                <Form.Select onChange={event=>setSpecializationId(event.target.value)} value={specializationId}>
                    <option value={0}>{specializations.length > 0 ? 'выберите специализацию' : ''}</option>
                    {specializations.map(sp=>{
                        return <option key={`sp_${sp.id}`} value={sp.id}>{sp.name}</option>
                    })}
                </Form.Select>
            </Form.Group>
            <Form.Group as={Row} className="mb-3">
                <Form.Label>Специалист:</Form.Label>
                <Form.Select onChange={event=>setWorkerId(event.target.value)} value={workerId}>
                    <option value={0}>{workers.length > 0 ? 'выберите специалиста' : ''}</option>
                    {workers.map(w=>{
                        return <option key={`sp_${w.id}`} value={w.id}>{w.name}</option>
                    })}
                </Form.Select>
            </Form.Group>
            <Form.Group as={Row} className="mb-3">
                <Form.Label>Процедура:</Form.Label>
                <Form.Select onChange={event=>setProcedureId(event.target.value)} value={procedureId}>
                    <option value={0}>{procedures.length > 0 ? 'выберите процедуру' : ''}</option>
                    {procedures.map(p=>{
                        return <option key={`pr_${p.id}`} value={p.id}>{p.name}</option>
                    })}
                </Form.Select>
            </Form.Group>
            <Form.Group as={Row} className="mb-3">
                <Form.Label>Рабочее время:</Form.Label>
                {schedules.map(s=>{
                    return <div key={`schedule_${s.id}`}>
                        <div>{s.date}</div>
                        <div>{s.location.name}</div>
                        <div>{s.location.address}</div>
                        <div>{s.start_work_time}</div>
                        <div>{s.finish_work_time}</div>
                    </div>
                })}
            </Form.Group>
        </Form>
    </Container>;
}

export default App;
