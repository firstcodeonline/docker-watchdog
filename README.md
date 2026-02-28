# Docker Watchdog

A lightweight Docker container monitoring system that sends real-time Telegram alerts when containers stop or recover. Perfect for DevOps teams and system administrators who need to stay informed about their containerized infrastructure.

## Features

- **Real-time Monitoring**: Continuously monitors all Docker containers on your system
- **Telegram Notifications**: Instant alerts sent directly to your Telegram chat
- **Status Tracking**: Detects when containers stop, exit, or pause
- **Recovery Alerts**: Notifies when containers come back online
- **Smart Alerting**: Prevents alert spam by tracking already-notified failures
- **Low Resource Usage**: Lightweight Python application running in a container
- **Auto-restart**: Configured to restart automatically if the watchdog itself fails

## Prerequisites

Before running Docker Watchdog, ensure you have:

- Docker Engine installed (version 20.10+)
- Docker Compose installed
- A Telegram Bot Token (see setup instructions below)
- Your Telegram Chat ID

## Setting Up Telegram Bot

1. **Create a Telegram Bot**:
   - Open Telegram and search for [@BotFather](https://t.me/botfather)
   - Send `/newbot` command
   - Follow the prompts to name your bot
   - Save the API token provided (format: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

2. **Get Your Chat ID**:
   - Start a chat with your new bot
   - Send any message to the bot
   - Visit: `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates`
   - Look for `"chat":{"id":` in the response
   - Save this numeric ID

## Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/firstcodeonline/docker-watchdog.git
   cd docker-watchdog
   ```

2. **Configure environment variables**:
   
   Copy the example file and edit with your credentials:
   ```bash
   cp .env.example .env
   ```
   
   Then edit `.env` with your values:
   ```bash
   TELEGRAM_TOKEN=your_telegram_bot_token_here
   TELEGRAM_CHAT_ID=your_chat_id_here
   ```

3. **Build and start the watchdog**:
   ```bash
   docker-compose up -d
   ```

4. **Verify it's running**:
   ```bash
   docker logs docker-watchdog
   ```
   You should see: `Docker Watchdog started... Monitoring containers.`

## How It Works

The Docker Watchdog operates by:

1. **Connecting to Docker**: Uses the Docker socket (`/var/run/docker.sock`) to communicate with the Docker daemon
2. **Polling Containers**: Checks all container statuses every 60 seconds
3. **Detecting Changes**: Identifies containers that are not in "running" state
4. **Sending Alerts**: Sends a Telegram message when a container fails
5. **Tracking State**: Maintains a set of failed containers to avoid duplicate alerts
6. **Recovery Notification**: Sends a recovery message when a failed container returns to running state

### Alert Examples

**Failure Alert**:
```
⚠️ DEVOPS ALERT
The container my-web-server is: exited
Check your server soon.
```

**Recovery Alert**:
```
✅ RECOVERED
The container my-web-server is back to life.
```

## Project Structure

```
docker-watchdog/
├── monitor.py           # Main monitoring script
├── Dockerfile          # Container image definition
├── docker-compose.yml  # Service orchestration
├── requirements.txt    # Python dependencies
├── .env.example       # Environment variables template
├── README.md          # This file
└── .env               # Environment variables (create this)
```

## Configuration

### Environment Variables

| Variable | Description | Required | Example |
|----------|-------------|----------|---------|
| `TELEGRAM_TOKEN` | Your Telegram bot API token | Yes | `123456789:ABCdefGHI...` |
| `TELEGRAM_CHAT_ID` | Your Telegram chat ID | Yes | `987654321` |
| `CHECK_INTERVAL` | Monitoring interval in seconds | No | `60` (default) |

### Changing Check Interval

To modify the monitoring frequency, edit `CHECK_INTERVAL` in `monitor.py`:

```python
CHECK_INTERVAL = 120  # Check every 2 minutes
```

Then rebuild the container:
```bash
docker-compose up -d --build
```

## Usage

### Start Monitoring
```bash
docker-compose up -d
```

### View Logs
```bash
docker logs -f docker-watchdog
```

### Stop Watchdog
```bash
docker-compose down
```

### Restart Watchdog
```bash
docker-compose restart
```

## Python Virtual Environment Setup (Optional)

If you prefer to run the monitor script locally without Docker, you can set up a Python virtual environment with a custom path.

### Creating a Virtual Environment with Custom Path

1. **Create virtual environment in a custom location**:
   ```bash
   python3 -m venv /path/to/your/custom/venv
   ```
   
   Example:
   ```bash
   python3 -m venv ~/environments/docker-watchdog-env
   ```

2. **Activate the virtual environment**:
   
   On macOS/Linux:
   ```bash
   source /path/to/your/custom/venv/bin/activate
   ```
   
   Example:
   ```bash
   source ~/environments/docker-watchdog-env/bin/activate
   ```
   
   On Windows:
   ```bash
   \path\to\your\custom\venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**:
   ```bash
   export TELEGRAM_TOKEN="your_token_here"
   export TELEGRAM_CHAT_ID="your_chat_id_here"
   ```

5. **Run the monitor**:
   ```bash
   python monitor.py
   ```

6. **Deactivate when done**:
   ```bash
   deactivate
   ```

### Creating Aliases for Quick Access

Add to your `~/.bashrc` or `~/.zshrc`:
```bash
alias watchdog-activate="source ~/environments/docker-watchdog-env/bin/activate"
```

Then simply run:
```bash
watchdog-activate
```

## Troubleshooting

### No alerts are being sent

1. **Check logs for errors**:
   ```bash
   docker logs docker-watchdog
   ```

2. **Verify environment variables**:
   ```bash
   docker exec docker-watchdog env | grep TELEGRAM
   ```

3. **Test Telegram connectivity**:
   Send a test message using your token:
   ```bash
   curl "https://api.telegram.org/bot<YOUR_TOKEN>/getMe"
   ```

### Permission denied on Docker socket

Ensure the Docker socket has appropriate permissions:
```bash
ls -la /var/run/docker.sock
```

The socket should be readable by the user running Docker.

### Container not detecting other containers

- Verify the Docker socket is mounted correctly in `docker-compose.yml`
- Ensure Docker daemon is running: `docker ps`

## Security Considerations

- **Environment Variables**: Never commit `.env` files to version control (use `.env.example` as template)
- **Socket Access**: The container has read-only access to the Docker socket
- **Token Protection**: Keep your Telegram bot token confidential
- **Network Isolation**: Consider running on a private network if monitoring sensitive infrastructure

## Dependencies

- **Python 3.9**: Base runtime environment
- **docker (6.1.3)**: Python Docker SDK for container interaction
- **requests (2.31.0)**: HTTP library for Telegram API calls

## Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation

## License

See the [LICENSE](LICENSE) file for details.

## Use Cases

- **Production Monitoring**: Keep track of critical production containers
- **Development Environments**: Monitor local development stacks
- **CI/CD Pipelines**: Alert on build container failures
- **Multi-container Applications**: Ensure all services in your stack are healthy
- **Learning DevOps**: Great starter project for understanding container monitoring

## Future Enhancements

Potential features for future versions:
- Support for multiple notification channels (Slack, Discord, Email)
- Web dashboard for container status
- Configurable alert thresholds and cooldowns
- Container health check integration
- Resource usage monitoring (CPU, memory)
- Historical data logging and analytics

---

**Built with ❤️ for the FirstCode community**