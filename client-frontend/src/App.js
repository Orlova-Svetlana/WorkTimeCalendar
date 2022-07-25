import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';
import {Col, Container, Row, Tab, Tabs} from "react-bootstrap";
import {useState} from "react";
import ProfessionalProfilePath from "./components/paths/ProfessionalProfilePath";
import SpecializationPath from "./components/paths/SpecializationPath";
import WorkerPath from "./components/paths/WorkerPath";
import LocationPath from "./components/paths/LocationPath";
import ProcedurePath from "./components/paths/ProcedurePath";

const App = () => {

    const [pathId, setPathId] = useState('');

    return <Container>
        <Row>
            <Col className={'my-3'}>
                <h3>Выберите начальный критерий поиска:</h3>
                <Tabs defaultActiveKey="" className="mb-3" onSelect={value=>setPathId(value)} activeKey={pathId}>
                    <Tab eventKey='p' title='Профессиональный профиль'>
                        {pathId === 'p' && <ProfessionalProfilePath />}
                    </Tab>
                    <Tab eventKey='s' title='Специализация'>
                        {pathId === 's' && <SpecializationPath />}
                    </Tab>
                    <Tab eventKey='w' title='Специалист'>
                        {pathId === 'w' && <WorkerPath />}
                    </Tab>
                    <Tab eventKey='l' title='Локация'>
                        {pathId === 'l' && <LocationPath />}
                    </Tab>
                    <Tab eventKey='pr' title='Процедура'>
                        {pathId === 'pr' && <ProcedurePath />}
                    </Tab>
                </Tabs>
            </Col>
        </Row>
    </Container>;
}

export default App;
