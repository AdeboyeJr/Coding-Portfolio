#include "pch.h"
#include "MyRaytraceRenderer.h"
#include "graphics/GrTexture.h"
#include <cmath>



CMyRaytraceRenderer::CMyRaytraceRenderer()
{
	m_window = NULL;
}

CMyRaytraceRenderer::~CMyRaytraceRenderer()
{
}

void CMyRaytraceRenderer::SetWindow(CWnd* p_window) 
{
	m_window = p_window;
}

bool CMyRaytraceRenderer::RendererStart()
{
	m_intersection.Initialize();
	m_mstack.clear();
	m_material = NULL;

	// We have to do all the matrix work ourselves.
	// Set up the matrix stack.
	CGrTransform t;
	t.SetLookAt(Eye().X(), Eye().Y(), Eye().Z(),
		Center().X(), Center().Y(), Center().Z(),
		Up().X(), Up().Y(), Up().Z());

	m_mstack.push_back(t);

	//// Add lights
	//float dimd = 0.5f;
	//GLfloat dim[] = { dimd, dimd, dimd, 1.0f };
	//GLfloat brightwhite[] = { 1.f, 1.f, 1.f, 1.0f };

	//AddLight(CGrPoint(1, 0.5, 1.2, 0),
	//	dim, brightwhite, brightwhite);

	return true;
}

void CMyRaytraceRenderer::RendererMaterial(CGrMaterial* p_material)
{
	m_material = p_material;
}

void CMyRaytraceRenderer::RendererPushMatrix()
{
	m_mstack.push_back(m_mstack.back());
}

void CMyRaytraceRenderer::RendererPopMatrix()
{
	m_mstack.pop_back();
}

void CMyRaytraceRenderer::RendererRotate(double angle, double x, double y, double z)
{
	m_mstack.back().SetRotate(angle, CGrPoint(x,y,z));

}

void CMyRaytraceRenderer::RendererTranslate(double x, double y, double z)
{
	m_mstack.back().SetTranslate(x,y,z);
}

//
// Name : CMyRaytraceRenderer::RendererEndPolygon()
// Description : End definition of a polygon. The superclass has
// already collected the polygon information
//

void CMyRaytraceRenderer::RendererEndPolygon()
{
	const std::list<CGrPoint>& vertices = PolyVertices();
	const std::list<CGrPoint>& normals = PolyNormals();
	const std::list<CGrPoint>& tvertices = PolyTexVertices();

	// Allocate a new polygon in the ray intersection system
	m_intersection.PolygonBegin();
	m_intersection.Material(m_material);

	if (PolyTexture())
	{
		m_intersection.Texture(PolyTexture());
	}

	std::list<CGrPoint>::const_iterator normal = normals.begin();
	std::list<CGrPoint>::const_iterator tvertex = tvertices.begin();

	for (std::list<CGrPoint>::const_iterator i = vertices.begin(); i != vertices.end(); i++)
	{
		if (normal != normals.end())
		{
			m_intersection.Normal(m_mstack.back() * *normal);
			normal++;
		}

		if (tvertex != tvertices.end())
		{
			m_intersection.TexVertex(*tvertex);
			tvertex++;
		}

		m_intersection.Vertex(m_mstack.back() * *i);


	}

	m_intersection.PolygonEnd();
}

bool CMyRaytraceRenderer::RendererEnd()
{
	m_intersection.LoadingComplete();


	double ymin = -tan(ProjectionAngle() / 2 * GR_DTOR);
	double yhit = -ymin * 2;

	double xmin = ymin * ProjectionAspect();
	double xwid = -xmin * 2;

	for (int r = 0; r < m_rayimageheight; r++)
	{
		for (int c = 0; c < m_rayimagewidth; c++)
		{
			double x = xmin + (c + 0.5) / m_rayimagewidth * xwid;
			double y = ymin + (r + 0.5) / m_rayimageheight * yhit;

			// Construct a Ray
			CRay ray(CGrPoint(0, 0, 0), Normalize3(CGrPoint(x, y, -1, 0)));

			CRayColor ray_color;

			RayColor(ray, ray_color, 3, NULL);

			//double t;  // Will be distance to intersection
			//CGrPoint intersect;  // Will be x,y,z location of intersection
			//const CRayIntersection::Object* nearest; // Pointer to intersecting object

			//if (m_intersection.Intersect(ray, 1e20, NULL, nearest, t, intersect))
			//{
			//	// We hit something...
			//	// Determine information about the intersection
			//	CGrPoint N;
			//	CGrMaterial* material;
			//	CGrTexture* texture;
			//	CGrPoint texcoord;

			//	m_intersection.IntersectInfo(ray, nearest, t, N, material, texture, texcoord);

			//	if (material != NULL)
			//	{
			//		m_intersection.Texture(texture);
			//		m_intersection.TexVertex(texcoord);


			//		// Ambient color
			//		m_rayimage[r][c* 3] = GLbyte(material->Ambient(0) * 255);
			//		m_rayimage[r][c * 3 + 1] = GLbyte(material->Ambient(1) * 255);
			//		m_rayimage[r][c * 3 + 2] = GLbyte(material->Ambient(2) * 255);

			//		// Add diffuse and specular color from light sources
			//		for (int l = 0; l < LightCnt(); l++)
			//		{

			//			// Construct a Ray
			//			CRay ray(intersect, Normalize3(GetLight(l).m_pos));
			//			double t2;  // Will be distance to intersection
			//			CGrPoint intersect2;  // Will be x,y,z location of intersection
			//			const CRayIntersection::Object* blockage; // Pointer to object blocking light

			//			// Determine if not in shadow
			//			if (!m_intersection.Intersect(ray, 1e50, nearest, blockage, t2, intersect2))
			//			{
			//				// Calculate light direction
			//				CGrPoint lightDir;

			//				lightDir = intersect - GetLight(l).m_pos;



			//				// Diffuse color
			//				m_rayimage[r][c * 3] += GLbyte(BlinnPhong(lightDir, GetLight(l).m_diffuse[0] * 255., intersect, N, material->Ambient(0), material->Diffuse(0), material->Specular(0), material->Shininess()).diffuse);
			//				m_rayimage[r][c * 3 + 1] += GLbyte(BlinnPhong(lightDir, GetLight(l).m_diffuse[1] * 255., intersect, N, material->Ambient(1), material->Diffuse(1), material->Specular(1), material->Shininess()).diffuse);
			//				m_rayimage[r][c * 3 + 2] += GLbyte(BlinnPhong(lightDir, GetLight(l).m_diffuse[2] * 255., intersect, N, material->Ambient(2), material->Diffuse(2), material->Specular(2), material->Shininess()).diffuse);

			//				// Specular color
			//				m_rayimage[r][c * 3] += GLbyte(BlinnPhong(lightDir, GetLight(l).m_specular[0] * 255., intersect, N, material->Ambient(0), material->Diffuse(0), material->Specular(0), material->Shininess()).specular);
			//				m_rayimage[r][c * 3 + 1] += GLbyte(BlinnPhong(lightDir, GetLight(l).m_specular[1] * 255., intersect, N, material->Ambient(1), material->Diffuse(1), material->Specular(1), material->Shininess()).specular);
			//				m_rayimage[r][c * 3 + 2] += GLbyte(BlinnPhong(lightDir, GetLight(l).m_specular[2] * 255., intersect, N, material->Ambient(2), material->Diffuse(2), material->Specular(2), material->Shininess()).specular);

			//			}


			//		}



			//	}


			//}
			//else
			//{
			//	// We hit nothing...
			//	m_rayimage[r][c * 3] = 0;
			//	m_rayimage[r][c * 3 + 1] = 0;
			//	m_rayimage[r][c * 3 + 2] = 0;
			//}

			m_rayimage[r][c * 3] = GLbyte(ray_color[0]);
			m_rayimage[r][c * 3 + 1] = GLbyte(ray_color[1]);
			m_rayimage[r][c * 3 + 2] = GLbyte(ray_color[2]);


			

			
		}

		if (r % 20 == 0)
		{
			m_window->Invalidate();
			m_window->UpdateWindow();
		}
	}



	return true;
}

CMyRaytraceRenderer::PhongPair CMyRaytraceRenderer::BlinnPhong(CGrPoint lightDir, float lightInt, CGrPoint position, CGrPoint normal, float Ka, float Kd, float Ks, float shininess)
{
	CGrPoint s = Normalize3(lightDir);
	CGrPoint v = Normalize3(-position);
	CGrPoint n = Normalize3(normal);
	CGrPoint h = Normalize3(v + s);
	float diffuse = Ka + Kd * lightInt * max(0.0, Dot2(n,s));
	float spec = Ks * pow(max(0.0,Dot2(n,h)), shininess);

	PhongPair pair;
	pair.diffuse = diffuse;
	pair.specular = spec;


	return pair;
}


void CMyRaytraceRenderer::RayColor(const CRay& p_ray, CRayColor& p_color, int p_recursive, const CRayIntersection::Object* p_ignore)
{
	double t;  // Will be distance to intersection
	CGrPoint intersect;  // Will be x,y,z location of intersection
	const CRayIntersection::Object* nearest; // Pointer to intersecting object

	if (m_intersection.Intersect(p_ray, 1e20, p_ignore, nearest, t, intersect))
	{
		// We hit something...
		// Determine information about the intersection
		CGrPoint N;
		CGrMaterial* material;
		CGrTexture* texture;
		CGrPoint texcoord;

		m_intersection.IntersectInfo(p_ray, nearest, t, N, material, texture, texcoord);

		if (material != NULL)
		{
			
			
			// Ambient color
			p_color[0] = material->Ambient(0) * 255;
			p_color[1] = material->Ambient(1) * 255;
			p_color[2] = material->Ambient(2) * 255;
		

			// Add texture if available
			if (texture != NULL)
			{

				CGrTexture& tex = *texture;


				// Get the texture coordinates
				int y = texcoord.Y() * tex.Height();
				int x = texcoord.X() * tex.Width();

			


				// Texture Color
				p_color[0] = material->Ambient(0) * tex[y][x * 3];
				p_color[1] = material->Ambient(1) * tex[y][x * 3 + 1];
				p_color[2] = material->Ambient(2) * tex[y][x * 3 + 2];

			}




			// Add diffuse and specular color from light sources
			for (int l = 0; l < LightCnt(); l++)
			{

				// Construct a Ray
				CRay ray(intersect, Normalize3(GetLight(l).m_pos));
				double t2;  // Will be distance to intersection
				CGrPoint intersect2;  // Will be x,y,z location of intersection
				const CRayIntersection::Object* blockage; // Pointer to object blocking light

				// Determine if not in shadow
				if (!m_intersection.Intersect(ray, 1e80, nearest, blockage, t2, intersect2))
				{
					// Calculate light direction
					CGrPoint lightDir;

					lightDir = intersect - GetLight(l).m_pos;

					// Diffuse color
					p_color[0] += BlinnPhong(lightDir, GetLight(l).m_diffuse[0] * 255., intersect, N, material->Ambient(0), material->Diffuse(0), material->Specular(0), material->Shininess()).diffuse;
					p_color[1] += BlinnPhong(lightDir, GetLight(l).m_diffuse[1] * 255., intersect, N, material->Ambient(1), material->Diffuse(1), material->Specular(1), material->Shininess()).diffuse;
					p_color[2] += BlinnPhong(lightDir, GetLight(l).m_diffuse[2] * 255., intersect, N, material->Ambient(2), material->Diffuse(2), material->Specular(2), material->Shininess()).diffuse;

					// Specular color
					p_color[0] += BlinnPhong(lightDir, GetLight(l).m_specular[0] * 255., intersect, N, material->Ambient(0), material->Diffuse(0), material->Specular(0), material->Shininess()).specular;
					p_color[1] += BlinnPhong(lightDir, GetLight(l).m_specular[1] * 255., intersect, N, material->Ambient(1), material->Diffuse(1), material->Specular(1), material->Shininess()).specular;
					p_color[2] += BlinnPhong(lightDir, GetLight(l).m_specular[2] * 255., intersect, N, material->Ambient(2), material->Diffuse(2), material->Specular(2), material->Shininess()).specular;

					
				}

				


			}

			if (p_recursive > 0 && (material->SpecularOther(0) > 0 || material->SpecularOther(1) > 0 || material->SpecularOther(2) > 0))
			{
				CGrPoint R;
				R = N * 2 * Dot3(N, -p_ray.Direction())  - (-p_ray.Direction());

				CRay ray(intersect, Normalize3(R));

				CRayColor color;

				// Recursive call
				RayColor(ray, color, p_recursive - 1, nearest);

				if (color[0] > 0 || color[1] > 0 || color[2] > 0)
				{
					p_color[0] = color[0] * material->SpecularOther(0);
					p_color[1] = color[1] * material->SpecularOther(1);
					p_color[2] = color[2] * material->SpecularOther(2);
				}


		
			}



		}


	}
	else
	{
	
		// We hit nothing...
		p_color[0] = 0;
		p_color[1] = 0;
		p_color[2] = 0;
		
	
	}


}



