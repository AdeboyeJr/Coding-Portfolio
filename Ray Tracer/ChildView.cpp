
// ChildView.cpp : implementation of the CChildView class
//

#include "pch.h"
#include "framework.h"
#include "Project1.h"
#include "ChildView.h"
#include "graphics/OpenGLRenderer.h"
#include "MyRaytraceRenderer.h"
#include "graphics/GrTexture.h"

#ifdef _DEBUG
#define new DEBUG_NEW
#endif


// CChildView

CChildView::CChildView()
{
	m_camera.Set(20, 10, 50, 0, 0, 0, 0, 1, 0);

	CGrPtr<CGrComposite> scene = new CGrComposite;
	m_scene = scene;

	CGrPtr<CGrTexture> texture = new CGrTexture;

	texture->LoadFile(L"textures/picnic.bmp");

	// A red box
	CGrPtr<CGrMaterial> redpaint = new CGrMaterial;
	redpaint->AmbientAndDiffuse(0.8f, 0.0f, 0.0f);
	redpaint->Specular(0.8f);
	redpaint->Shininess(100.f);
	redpaint->SpecularOther(0.8f, 0.8f, 0.8f);
	scene->Child(redpaint);

	CGrPtr<CGrComposite> redbox = new CGrComposite;
	redpaint->Child(redbox);
	redbox->Box(-5, 1, -5, 5, 5, 5);


	// A yellow box
	CGrPtr<CGrMaterial> yellowpaint = new CGrMaterial;
	yellowpaint->AmbientAndDiffuse(0.8f, 0.8f, 0.0f);
	yellowpaint->Specular(0.8f);
	yellowpaint->Shininess(50.f);
	//yellowpaint->SpecularOther(0.4f, 0.4f, 0.4f);
	scene->Child(yellowpaint);

	CGrPtr<CGrComposite> yellowbox = new CGrComposite;
	yellowpaint->Child(yellowbox);
	yellowbox->Box(-15, 2, -10, 5, 5, 5);

	// A blue pyramid
	CGrPtr<CGrMaterial> bluepaint = new CGrMaterial;
	bluepaint->AmbientAndDiffuse(0.0f, 0.0f, 0.8f);
	bluepaint->Specular(0.8f);
	bluepaint->Shininess(50.f);
	bluepaint->SpecularOther(0.8f, 0.8f, 0.8f);
	scene->Child(bluepaint);

	CGrPtr<CGrComposite> bluepyramid = new CGrComposite;
	bluepaint->Child(bluepyramid);
	bluepyramid->Pyramid(-15, 2, -20, 5, 5, 5);

	// Purple Slanted Box
	CGrPtr<CGrMaterial> purplepaint = new CGrMaterial;
	purplepaint->AmbientAndDiffuse(0.8f, 0.0f, 0.8f);
	purplepaint->Specular(0.8f);
	purplepaint->Shininess(50.f);
	//purplepaint->SpecularOther(0.8f, 0.8f, 0.8f);
	scene->Child(purplepaint);

	CGrPtr<CGrComposite> slantedBox = new CGrComposite;
	purplepaint->Child(slantedBox);
	slantedBox->SlantBox(-15, 7, -5, 5, 5, 5, 2);


	// Textured Plane
	CGrPtr<CGrMaterial> clearpaint = new CGrMaterial;
	clearpaint->AmbientAndDiffuse(.6f, .6f, .6, .6f);
	clearpaint->Specular(0.8f);
	clearpaint->Shininess(10.f);
	//clearpaint->SpecularOther(0.8f, 0.8f, 0.8f);
	scene->Child(clearpaint);



	
	

	CGrPtr<CGrComposite> plane = new CGrComposite;
	clearpaint->Child(plane);
	plane->Plane(-20, 0, -20, 20, 20, 20, texture);
	plane->Child(texture);
	




	m_raytrace = false;

	m_rayimage = NULL;

}

CChildView::~CChildView()
{
	delete m_rayimage;
}


BEGIN_MESSAGE_MAP(CChildView, COpenGLWnd)
	ON_WM_PAINT()
	ON_WM_LBUTTONDOWN()
	ON_WM_MOUSEMOVE()
	ON_WM_RBUTTONDOWN()
	ON_COMMAND(ID_RENDER_RAYTRACE, &CChildView::OnRenderRaytrace)
	ON_UPDATE_COMMAND_UI(ID_RENDER_RAYTRACE, &CChildView::OnUpdateRenderRaytrace)
END_MESSAGE_MAP()



// CChildView message handlers

BOOL CChildView::PreCreateWindow(CREATESTRUCT& cs) 
{
	if (!COpenGLWnd::PreCreateWindow(cs))
		return FALSE;

	cs.dwExStyle |= WS_EX_CLIENTEDGE;
	cs.style &= ~WS_BORDER;
	cs.lpszClass = AfxRegisterWndClass(CS_HREDRAW|CS_VREDRAW|CS_DBLCLKS, 
		::LoadCursor(nullptr, IDC_ARROW), reinterpret_cast<HBRUSH>(COLOR_WINDOW+1), nullptr);

	return TRUE;
}




void CChildView::OnGLDraw(CDC* pDC)
{
	if (m_raytrace)
	{
		// Clear the color buffer
		glClearColor(0.0f, 0.0f, 0.0f, 0.0f);
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

		// Set up for parallel projection
		int width, height;
		GetSize(width, height);

		glMatrixMode(GL_PROJECTION);
		glLoadIdentity();
		glOrtho(0, width, 0, height, -1, 1);

		glMatrixMode(GL_MODELVIEW);
		glLoadIdentity();

		// If we got it, draw it
		if (m_rayimage)
		{
			glRasterPos3i(0, 0, 0);
			glDrawPixels(m_rayimagewidth, m_rayimageheight,
				GL_RGB, GL_UNSIGNED_BYTE, m_rayimage[0]);
		}

		glFlush();
	}
	else
	{
		//
		// Instantiate a renderer
		//

		COpenGLRenderer renderer;

		// Configure the renderer
		ConfigureRenderer(&renderer);

		//
		// Render the scene
		//

		renderer.Render(m_scene);
	}


}


void CChildView::OnLButtonDown(UINT nFlags, CPoint point)
{
	m_camera.MouseDown(point.x, point.y);

	COpenGLWnd::OnLButtonDown(nFlags, point);
}




void CChildView::OnMouseMove(UINT nFlags, CPoint point)
{
	if (m_camera.MouseMove(point.x, point.y, nFlags))
		Invalidate();


	COpenGLWnd::OnMouseMove(nFlags, point);
}



void CChildView::OnRButtonDown(UINT nFlags, CPoint point)
{
	m_camera.MouseDown(point.x, point.y, 2);

	COpenGLWnd::OnRButtonDown(nFlags, point);
}

//
// Name :         CChildView::ConfigureRenderer()
// Description :  Configures our renderer so it is able to render the scene.
//                Indicates how we'll do our projection, where the camera is,
//                and where any lights are located.
//

void CChildView::ConfigureRenderer(CGrRenderer* p_renderer)
{
	// Determine the screen size so we can determine the aspect ratio
	int width, height;
	GetSize(width, height);
	double aspectratio = double(width) / double(height);

	// 
	// Set upt he camera in the renderer
	//

	p_renderer->Perspective(m_camera.FieldOfView(),
		aspectratio, // The aspect ratio.
		20., // Near clipping
		1000.); // Far clipping

	// m_camera.FieldOfView is the vertical field of view in degrees.

	//
	// Set the camera location
	//

	p_renderer->LookAt(m_camera.Eye()[0], m_camera.Eye()[1],
		m_camera.Eye()[2],
		m_camera.Center()[0], m_camera.Center()[1],
		m_camera.Center()[2],
		m_camera.Up()[0], m_camera.Up()[1], m_camera.Up()[2]);

	//
	// Set the light locations and colors
	//

	float dimd = 0.5f;
	GLfloat dim[] = { dimd, dimd, dimd, 1.0f };
	GLfloat brightwhite[] = { 1.f, 1.f, 1.f, 1.0f };

	p_renderer->AddLight(CGrPoint(1, 0.5, 1.2, 0),
		dim, brightwhite, brightwhite);

	GLfloat brightred[] = { 1.f, 0.f, 0.f, 1.0f };

	p_renderer->AddLight(CGrPoint(-1, 0.5, 1.2, 0),
		dim, brightred, brightred);

}


void CChildView::OnRenderRaytrace()
{
	m_raytrace = !m_raytrace;
	Invalidate();
	if (!m_raytrace)
		return;

	GetSize(m_rayimagewidth, m_rayimageheight);

	m_rayimage = new BYTE * [m_rayimageheight];

	int rowwid = m_rayimagewidth * 3;
	while (rowwid % 4)
		rowwid++;

	m_rayimage[0] = new BYTE[m_rayimageheight * rowwid];

	for (int i = 1; i < m_rayimageheight; i++)
	{
		m_rayimage[i] = m_rayimage[0] + i * rowwid;
	}

	for (int i = 0; i < m_rayimageheight; i++)
	{
		// Fill the image with blue
		for(int j=0; j<m_rayimagewidth; j++)
		{
			m_rayimage[i][j * 3] = 0;    // red
			m_rayimage[i][j * 3 + 1] = 0; // green
			m_rayimage[i][j * 3 + 2] = 0; // blue
		}
	}

	// Instantiate a raytrace object
	CMyRaytraceRenderer raytrace;

	// Generic configurations for all renderers
	ConfigureRenderer(&raytrace);

	//
	// Render the Scene
	//

	raytrace.SetImage(m_rayimage, m_rayimagewidth, m_rayimageheight);
	raytrace.SetWindow(this);
	raytrace.Render(m_scene);
	Invalidate();

}


void CChildView::OnUpdateRenderRaytrace(CCmdUI* pCmdUI)
{
	pCmdUI->SetCheck(m_raytrace);

	if(m_rayimage)
		m_rayimage = NULL;
}
