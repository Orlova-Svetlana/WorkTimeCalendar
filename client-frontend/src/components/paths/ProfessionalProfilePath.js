import React, {useEffect, useState} from 'react'
import axios from "axios";
import {API_ADDRESS} from "../../constants";
import {Accordion, Button, Form} from "react-bootstrap";
import Select from "../selects/Select";
import AppointmentFormModal from "./AppointmentFormModal";

const ProfessionalProfilePath = () => {

    const [fetchingProfiles, setFetchingProfiles] = useState(false);
    const [profiles, setProfiles] = useState([]);
    const [profileId, setProfileId] = useState(0);

    const [fetchingSpecializations, setFetchingSpecializations] = useState(false);
    const [specializations, setSpecializations] = useState([]);
    const [specializationId, setSpecializationId] = useState(0);

    const [fetchingWorkers, setFetchingWorkers] = useState(false);
    const [workers, setWorkers] = useState([]);
    const [workerId, setWorkerId] = useState(0);

    const [fetchingProcedures, setFetchingProcedures] = useState(false);
    const [procedures, setProcedures] = useState([]);
    const [procedureId, setProcedureId] = useState(0);

    const [fetchingSchedules, setFetchingSchedules] = useState(false);
    const [schedules, setSchedules] = useState([]);

    useEffect(() => {
        setFetchingProfiles(true);
        axios.get(`${API_ADDRESS}professionalprofiles/`).then(response => {
            setFetchingProfiles(false);
            setProfiles(response.data);
        });
        return () => {
            setProfiles([]);
        };
    }, []);

    useEffect(() => {
        setProfileId(0)
    }, [profiles]);

    useEffect(() => {
        setSpecializationId(0);
        setFetchingSpecializations(true);
        setSpecializations([]);
        if (profileId > 0) {
            axios.get(`${API_ADDRESS}specializations/?professional_profile=${profileId}`).then(response => {
                setFetchingSpecializations(false);
                setSpecializations(response.data);
            });
        }
    }, [profileId]);

    useEffect(() => {
        setWorkerId(0);
        setProcedureId(0);
        setFetchingWorkers(true);
        setWorkers([]);
        setFetchingProcedures(true);
        setProcedures([]);
        if (specializationId > 0) {
            axios.get(`${API_ADDRESS}workers/?specialization=${specializationId}`).then(response => {
                setFetchingWorkers(false);
                setWorkers(response.data);
            });

            axios.get(`${API_ADDRESS}procedures/?specialization=${specializationId}`).then(response => {
                setFetchingProcedures(false);
                setProcedures(response.data.map(p=>{
                    p.name = `${p.name} (${p.duration} min)`;
                    return p;
                }));
            });
        }
    }, [specializationId]);

    const getWorkerSchedulers = () => {
        axios.get(`${API_ADDRESS}schedules/?worker=${workerId}`).then(response => {
                setFetchingSchedules(false);

                const dates = {};
                response.data.map(d=>{
                    if (!dates.hasOwnProperty(d.date)) {
                        dates[d.date] = {
                            date: d.date,
                            locations: {}
                        }
                    }
                    dates[d.date].locations[d.location.id] = {
                        ...d.location,
                        schedules: []
                    };
                    dates[d.date].locations[d.location.id].schedules.push({
                        id: d.id,
                        date: d.date,
                        start_work_time: d.start_work_time,
                        finish_work_time: d.finish_work_time,
                        appointments: d.appointments,
                    })
                });
                setSchedules(Object.values(dates));
            });
    };

    useEffect(() => {
        setFetchingSchedules(true);
        setSchedules([]);
        if (workerId > 0) {
            getWorkerSchedulers();
        }
    }, [workerId]);

    const dateToTimeString = (d) => {
        return ("0" + d.getHours()).slice(-2) + ":" + ("0" + d.getMinutes()).slice(-2) + ":" + ("0" + d.getSeconds()).slice(-2);
    };

    const onSelectSegment = (selectedProcedureId, selectedScheduleId, selectedSegment) => {
        setSelectedScheduleId(Number(selectedScheduleId));
        setSelectedSegment(selectedSegment);
        let date = null;
        for (const s of schedules) {
            for (const l of Object.values(s.locations)) {
                for (const sch of Object.values(l.schedules)) {
                    if (sch.id === selectedScheduleId) {
                        date = sch.date;
                    }
                }
            }
        }
        setSelectedScheduleDate(date)
    };

    const [showModal, setShowModal] = useState(false);
    const [selectedScheduleId, setSelectedScheduleId] = useState(0);
    const [selectedSegment, setSelectedSegment] = useState(null);
    const [selectedScheduleDate, setSelectedScheduleDate] = useState(null);

    useEffect(()=>{
        if (selectedScheduleId > 0 && selectedSegment && selectedScheduleDate.length > 0) {
            setShowModal(true);
        }
    }, [selectedScheduleId, selectedSegment, selectedScheduleDate])

    return <React.Fragment>
        <Form>
            {showModal === true && <AppointmentFormModal
                setShowModal={setShowModal}
                procedureId={procedureId}
                procedureName={procedures.find(p=>p.id===procedureId).name}
                selectedScheduleDate={selectedScheduleDate}
                selectedScheduleId={selectedScheduleId}
                selectedSegment={selectedSegment}
                onClose={()=> setShowModal(false)}
                onSuccess={()=> {
                    setShowModal(false);
                    getWorkerSchedulers();
                }}
            />}
            <Form.Group className="mb-3">
                <Select
                    placeholder={'выберите профиль'}
                    fetching={fetchingProfiles}
                    data={profiles}
                    onChange={(event) => setProfileId(event.target.value)}
                    selectedId={profileId}
                />
            </Form.Group>
            {profileId > 0 && <Form.Group className="mb-3">
                <Select
                    formLabel={'Специализация'}
                    placeholder={'выберите специализацию'}
                    fetching={fetchingSpecializations || specializations.length === 0}
                    data={specializations}
                    onChange={(event) => setSpecializationId(event.target.value)}
                    selectedId={specializationId}
                />
            </Form.Group>}
            {specializationId > 0 && <Form.Group className="mb-3">
                <Select
                    formLabel={'Специалист'}
                    placeholder={'выберите специалиста'}
                    fetching={fetchingWorkers || (workers.length === 0)}
                    data={workers}
                    onChange={(event) => setWorkerId(event.target.value)}
                    selectedId={workerId}
                />
            </Form.Group>}
            {workerId > 0 && <Form.Group className="mb-3">
                <Select
                    formLabel={'Процедура'}
                    placeholder={'выберите процедуру'}
                    fetching={fetchingProcedures || (procedures.length === 0)}
                    data={procedures}
                    onChange={(event) => setProcedureId(Number(event.target.value))}
                    selectedId={procedureId}
                />
            </Form.Group>}
            {schedules.length > 0 && <Form.Group className="mb-3">
                <Form.Label>Рабочее время:</Form.Label>
                <Accordion alwaysOpen>
                    {schedules.length > 0 && schedules.map((s, sIndex) => {
                        return <Accordion.Item key={`key_${sIndex}`} eventKey={`key_${sIndex}`}>
                            <Accordion.Header>
                                <div className="d-flex w-100">
                                    <div className="flex-grow-1">{s.date}</div>
                                    {/*<div>*/}
                                    {/*    <div className="btn btn-link btn-sm me-2" onClick={(event)=>{*/}
                                    {/*        event.stopPropagation()*/}
                                    {/*        onDateEditClick(s.id);*/}
                                    {/*    }}>Edit</div>*/}
                                    {/*    {Object.keys(s.locations).length === 0 && <div onClick={(event)=>{*/}
                                    {/*        event.stopPropagation()*/}
                                    {/*        onDateDeleteClick(s.id);*/}
                                    {/*    }} className="btn btn-link btn-sm me-2">Delete</div>}*/}
                                    {/*</div>*/}
                                </div>
                            </Accordion.Header>
                            <Accordion.Body>
                                <Accordion alwaysOpen>
                                    {Object.values(s.locations).map(l=>{
                                        return <Accordion.Item key={`key_${l.id}`} eventKey={`key_${l.id}`}>
                                            <Accordion.Header>
                                                <div className="d-flex w-100">
                                                    <div className="flex-grow-1">{l.name} {l.address}</div>
                                                    {/*<div>*/}
                                                    {/*    <div className="btn btn-link btn-sm me-2" onClick={(event)=>{*/}
                                                    {/*        event.stopPropagation()*/}
                                                    {/*        onLocationEditClick(s.id, l.id);*/}
                                                    {/*    }}>Edit</div>*/}
                                                    {/*    {Object.keys(l.schedules).length === 0 && <div  onClick={(event)=>{*/}
                                                    {/*        event.stopPropagation()*/}
                                                    {/*        onLocationDeleteClick(s.id, l.id);*/}
                                                    {/*    }} className="btn btn-link btn-sm me-2">Delete</div>}*/}
                                                    {/*</div>*/}
                                                </div>
                                            </Accordion.Header>
                                            <Accordion.Body>
                                                <Accordion alwaysOpen>
                                                    {Object.values(l.schedules).map(sch=>{
                                                        const segments = [];
                                                        for (const a of sch.appointments) {
                                                            const aStartTime = new Date(s.date + ' ' + a.procedure_start_time);
                                                            const aEndTime = new Date(s.date + ' ' + a.procedure_end_time);
                                                            segments.push({start: aStartTime, end: aEndTime, used: true});
                                                        }

                                                        if (procedureId > 0) {
                                                            const procedure = procedures.find(p=>Number(p.id)===Number(procedureId));
                                                            if (procedure) {
                                                                const duration = procedure.duration;
                                                                const schStartDateTime = new Date(s.date + ' ' + sch.start_work_time);
                                                                const schEndDateTime = new Date(s.date + ' ' + sch.finish_work_time);
                                                                const minutes = Math.abs(schEndDateTime.getTime() - schStartDateTime.getTime()) / 1000 / 60;
                                                                for (let m = 0; m <= (minutes - duration); m += 5) {
                                                                    const segmentStart = new Date(s.date + ' ' + sch.start_work_time);
                                                                    segmentStart.setMinutes(segmentStart.getMinutes() + m);

                                                                    const segmentEnd = new Date(segmentStart.getTime());
                                                                    segmentEnd.setMinutes(segmentEnd.getMinutes() + duration);

                                                                    let valid = true;

                                                                    for (const a of sch.appointments) {
                                                                        const aStartTime = (new Date(s.date + ' ' + a.procedure_start_time)).getTime();
                                                                        const aEndTime = (new Date(s.date + ' ' + a.procedure_end_time)).getTime();

                                                                        if (
                                                                            (segmentStart.getTime() < aStartTime && segmentEnd.getTime() <= aStartTime)
                                                                            ||
                                                                            (segmentStart.getTime() >= aEndTime && segmentEnd.getTime() > aEndTime)
                                                                        ) {

                                                                        } else {
                                                                            valid = false;
                                                                            break;
                                                                        }
                                                                    }
                                                                    if (valid) {
                                                                        segments.push({start: segmentStart, end: segmentEnd, used: false});
                                                                    }
                                                                }
                                                            }
                                                        }

                                                        return <Accordion.Item key={`key_${sch.id}`} eventKey={`key_${sch.id}`}>
                                                            <Accordion.Header>
                                                                <div className="d-flex w-100">
                                                                    <div className="flex-grow-1">{sch.start_work_time} - {sch.finish_work_time}</div>
                                                                    {/*<div>*/}
                                                                    {/*    <div className="btn btn-link btn-sm me-2" onClick={(event)=>{*/}
                                                                    {/*        event.stopPropagation()*/}
                                                                    {/*        onScheduleEditClick(s.id, l.id, sch.id);*/}
                                                                    {/*    }}>Edit</div>*/}
                                                                    {/*    {sch.appointments.length === 0 && <div className="btn btn-link btn-sm me-2" onClick={(event)=>{*/}
                                                                    {/*        event.stopPropagation()*/}
                                                                    {/*        onScheduleDeleteClick(s.id, l.id, sch.id);*/}
                                                                    {/*    }}>Delete</div>}*/}
                                                                    {/*</div>*/}
                                                                </div>
                                                            </Accordion.Header>
                                                            <Accordion.Body>
                                                                <Accordion alwaysOpen>
                                                                    {segments && segments.sort((a, b)=>a.start - b.start).map((segment, index)=>{
                                                                        if (segment.used) {
                                                                            return <Button key={`segment_${index}`} className={`me-2 mb-2 segment-button segment-used`} variant={'secondary'} disabled={true}>
                                                                                {dateToTimeString(segment.start)} - {dateToTimeString(segment.end)}
                                                                            </Button>
                                                                        }
                                                                        return <Button onClick={()=>onSelectSegment(procedureId, sch.id, dateToTimeString(segment.start))} key={`segment_${index}`} className={`me-2 mb-2 segment-button segment-empty`} variant={'primary'}>
                                                                            {dateToTimeString(segment.start)} - {dateToTimeString(segment.end)}
                                                                        </Button>
                                                                    })}
                                                                </Accordion>
                                                            </Accordion.Body>
                                                        </Accordion.Item>
                                                    })}
                                                </Accordion>
                                            </Accordion.Body>
                                        </Accordion.Item>
                                    })}
                                </Accordion>
                            </Accordion.Body>
                        </Accordion.Item>
                    })}
                </Accordion>
            </Form.Group>}
        </Form>
    </React.Fragment>
};

export default ProfessionalProfilePath;