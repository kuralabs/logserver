import React, { Component } from 'react'


class App extends Component {

    constructor(props) {
        super(props)
        this.ws = null
        this.bottomRef = React.createRef();
        this.state = {
            lines: [],
        }

        this.onWsMessage = this.onWsMessage.bind(this);
    }

    async onWsMessage(event) {
        this.setState({
            lines: [...this.state.lines, event.data],
        });
    }

    componentDidMount() {
        const { host, filename } = this.props

        this.ws = new WebSocket(`ws://${host}/follow/${filename}`);
        this.ws.onmessage = this.onWsMessage
    }

    componentWillUnmount() {
        this.ws.close()
        this.ws = null
    }

    componentDidUpdate() {
        this.bottomRef.current.scrollIntoView();
    }

    render() {
        const { lines } = this.state

        return (
            <div id="messages">
                {
                    lines.map((line, index) =>
                        <span key={ index }>{ line }</span>
                    )
                }
                <span ref={ this.bottomRef } />
            </div>
        )
    }
}

App.defaultProps = {
    host: 'localhost:9292',
    filename: 'afile.log',
}

export default App
