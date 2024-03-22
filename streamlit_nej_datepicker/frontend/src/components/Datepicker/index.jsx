import {
    Streamlit,
    StreamlitComponentBase,
    withStreamlitConnection,
} from "streamlit-component-lib"
import Datepicker from "@nejadipour/react-modern-datepicker";


class DatepickerClass extends StreamlitComponentBase {
    constructor(props) {
        super(props);
        this.onChange = this.onChange.bind(this);
        this.state = {
            open: false
        }
    }

    onChange(value) {
        this.setState(
            {value},
            () => Streamlit.setComponentValue(value)
        )
    }

    onRenderReady = () => {
        Streamlit.setComponentReady()
    }

    render() {
        return (
            <span style={{margin: 7}}>
                    <Datepicker {...this.props?.args?.config} onChange={this.onChange} popover={false}
                                onRenderReady={this.onRenderReady} disabled={this.props.disabled}/>
            </span>
        )
    }
}

const ConnectedDatepickerClass = withStreamlitConnection(DatepickerClass);

export default ConnectedDatepickerClass;
