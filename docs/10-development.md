# Development Guide

Guide for developers contributing to or extending the Autism Emotion Detection project.

## 📋 Table of Contents

- [Development Setup](#development-setup)
- [Code Structure](#code-structure)
- [Contributing Guidelines](#contributing-guidelines)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Git Workflow](#git-workflow)
- [Release Process](#release-process)
- [Project Roadmap](#project-roadmap)

## 🛠️ Development Setup

### Prerequisites

- Python 3.8+
- Node.js 14+
- Git
- Code editor (VS Code recommended)
- Virtual environment tool

### Initial Setup

1. **Clone Repository**
   ```bash
   git clone <repository-url>
   cd Autism-Emotion-Detection
   ```

2. **Backend Setup**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```

3. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   ```

4. **Development Mode**
   ```bash
   # Terminal 1 - Backend
   cd backend
   python app.py  # Runs with debug=True

   # Terminal 2 - Frontend
   cd frontend
   npm start  # Hot reload enabled
   ```

## 📁 Code Structure

### Project Organization

```
Autism-Emotion-Detection/
├── backend/              # Flask backend
│   ├── app.py           # Main application
│   └── requirements.txt # Python dependencies
├── frontend/            # React frontend
│   ├── src/
│   │   ├── App.js
│   │   └── components/
│   └── package.json
├── scripts/             # Training scripts
│   ├── train_advanced_model.py
│   ├── train_fast_model.py
│   └── ...
├── models/              # Trained models
├── docs/                # Documentation
└── README.md            # Project README
```

### Backend Structure

```
backend/
├── app.py               # Flask app, routes, model loading
└── requirements.txt     # Dependencies
```

**Key Functions**:
- `load_custom_model()` - Model loading logic
- `detect_face()` - Face detection
- `preprocess_image()` - Image preprocessing
- `predict_with_custom_model()` - Model inference
- Route handlers for API endpoints

### Frontend Structure

```
frontend/src/
├── App.js              # Main app component
├── components/
│   └── EmotionDetector.js  # Main detection component
└── index.js            # React entry point
```

**Key Components**:
- `App` - Main application wrapper
- `EmotionDetector` - Detection logic and UI

## 🤝 Contributing Guidelines

### Getting Started

1. **Fork the Repository**
   - Create your own fork
   - Clone your fork locally

2. **Create Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make Changes**
   - Follow coding standards
   - Write clear commit messages
   - Test your changes

4. **Submit Pull Request**
   - Push to your fork
   - Create PR with description
   - Reference related issues

### Contribution Areas

- **Bug Fixes**: Fix issues and improve stability
- **Features**: Add new functionality
- **Documentation**: Improve docs
- **Testing**: Add tests
- **Performance**: Optimize code
- **UI/UX**: Improve interface

### Pull Request Guidelines

**PR Title**: Clear, descriptive title
**Description**: 
- What changes were made
- Why changes were needed
- How to test changes
- Screenshots (if UI changes)

**Code Quality**:
- Follow coding standards
- Add comments for complex logic
- Update documentation if needed
- Ensure no breaking changes (or document them)

## 📝 Coding Standards

### Python (Backend)

**Style**: Follow PEP 8

**Naming**:
- Functions: `snake_case`
- Classes: `PascalCase`
- Constants: `UPPER_SNAKE_CASE`

**Example**:
```python
def detect_face(image):
    """Detect face in image using Haar Cascade.
    
    Args:
        image: Input image array
        
    Returns:
        Tuple of (face_roi, face_coordinates)
    """
    # Implementation
    pass
```

**Best Practices**:
- Use type hints where helpful
- Add docstrings to functions
- Handle errors gracefully
- Use meaningful variable names

### JavaScript (Frontend)

**Style**: Follow ESLint React rules

**Naming**:
- Components: `PascalCase`
- Functions: `camelCase`
- Constants: `UPPER_SNAKE_CASE`

**Example**:
```javascript
const EmotionDetector = ({ apiUrl }) => {
  const [emotion, setEmotion] = useState(null);
  
  const detectEmotion = async () => {
    // Implementation
  };
  
  return (
    // JSX
  );
};
```

**Best Practices**:
- Use functional components
- Use hooks for state management
- Handle async operations properly
- Add error handling
- Use meaningful variable names

### Code Comments

**When to Comment**:
- Complex algorithms
- Non-obvious logic
- Workarounds or hacks
- Public API functions

**Comment Style**:
```python
# Python: Use docstrings
def function_name():
    """Brief description.
    
    Longer description if needed.
    """
    pass
```

```javascript
// JavaScript: Use JSDoc for functions
/**
 * Detects emotion from image
 * @param {string} imageData - Base64 encoded image
 * @returns {Promise<Object>} Emotion prediction results
 */
async function detectEmotion(imageData) {
  // Implementation
}
```

## 🧪 Testing

### Backend Testing

**Manual Testing**:
```bash
# Test health endpoint
curl http://localhost:5000/api/health

# Test detection endpoint
curl -X POST http://localhost:5000/api/detect-emotion \
  -H "Content-Type: application/json" \
  -d '{"image": "..."}'
```

**Python Testing** (if implemented):
```python
import pytest
from app import app

def test_health_endpoint():
    with app.test_client() as client:
        response = client.get('/api/health')
        assert response.status_code == 200
```

### Frontend Testing

**Manual Testing**:
- Test camera functionality
- Test image upload
- Test error handling
- Test different browsers

**React Testing** (if implemented):
```javascript
import { render, screen } from '@testing-library/react';
import EmotionDetector from './EmotionDetector';

test('renders emotion detector', () => {
  render(<EmotionDetector apiUrl="http://localhost:5000" />);
  const button = screen.getByText(/start camera/i);
  expect(button).toBeInTheDocument();
});
```

### Integration Testing

Test full workflow:
1. Start backend
2. Start frontend
3. Test camera detection
4. Test image upload
5. Verify results display

## 🔀 Git Workflow

### Branch Strategy

- `main` - Production-ready code
- `develop` - Development branch (if used)
- `feature/*` - New features
- `bugfix/*` - Bug fixes
- `hotfix/*` - Urgent fixes

### Commit Messages

**Format**:
```
Type: Brief description

Longer description if needed
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Tests
- `chore`: Maintenance

**Examples**:
```
feat: Add transfer learning support

fix: Resolve model loading path issue

docs: Update API documentation
```

### Workflow Steps

1. **Create Branch**
   ```bash
   git checkout -b feature/new-feature
   ```

2. **Make Changes**
   - Write code
   - Test changes
   - Update docs

3. **Commit Changes**
   ```bash
   git add .
   git commit -m "feat: Add new feature"
   ```

4. **Push and PR**
   ```bash
   git push origin feature/new-feature
   # Create PR on GitHub
   ```

## 🚀 Release Process

### Version Numbering

Follow Semantic Versioning: `MAJOR.MINOR.PATCH`

- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes

### Release Checklist

- [ ] All tests passing
- [ ] Documentation updated
- [ ] Version numbers updated
- [ ] CHANGELOG updated
- [ ] Release notes prepared
- [ ] Tag created: `git tag v1.0.0`
- [ ] Tag pushed: `git push origin v1.0.0`

### Release Steps

1. **Update Version**
   - `package.json` (frontend)
   - `README.md`
   - Documentation

2. **Create Release Branch**
   ```bash
   git checkout -b release/v1.0.0
   ```

3. **Final Testing**
   - Run all tests
   - Manual testing
   - Documentation review

4. **Merge and Tag**
   ```bash
   git checkout main
   git merge release/v1.0.0
   git tag v1.0.0
   git push origin main --tags
   ```

## 🗺️ Project Roadmap

### Current Features

- ✅ Real-time camera detection
- ✅ Image upload
- ✅ Custom model training
- ✅ Web interface
- ✅ REST API

### Planned Features

- [ ] User authentication
- [ ] Emotion history tracking
- [ ] Batch processing
- [ ] Model versioning
- [ ] Performance metrics dashboard
- [ ] Mobile app support
- [ ] Multi-language support

### Areas for Improvement

- **Performance**: GPU acceleration, model optimization
- **Accuracy**: Transfer learning, ensemble methods
- **UI/UX**: Better visualizations, accessibility
- **Testing**: Automated tests, CI/CD
- **Documentation**: More examples, tutorials

## 📚 Development Resources

### Documentation

- [Architecture](03-architecture.md) - System design
- [API Reference](06-api-reference.md) - API details
- [Training Guide](05-training-guide.md) - Model training

### External Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [React Documentation](https://react.dev/)
- [TensorFlow Documentation](https://www.tensorflow.org/)
- [Tailwind CSS Documentation](https://tailwindcss.com/)

## 🔗 Related Documentation

- [Installation Guide](02-installation.md) - Setup
- [Architecture](03-architecture.md) - System design
- [API Reference](06-api-reference.md) - API details
- [Troubleshooting](09-troubleshooting.md) - Common issues

---

**Next**: FAQ in [FAQ](11-faq.md)

