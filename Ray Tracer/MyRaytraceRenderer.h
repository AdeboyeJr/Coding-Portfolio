#pragma once
#include "graphics/GrRenderer.h"
#include "graphics/RayIntersection.h"
#include "graphics/GrTransform.h"
#include <list>

class CMyRaytraceRenderer :
    public CGrRenderer
{
public:
    CMyRaytraceRenderer();
    ~CMyRaytraceRenderer();


    void SetImage(BYTE** image, int w, int h) {
        m_rayimage = image;
        m_rayimagewidth = w;
        m_rayimageheight = h;
    }



    void SetWindow(CWnd* p_window);

    bool RendererStart();

    void RendererMaterial(CGrMaterial* p_material);

    void RendererPushMatrix();
    void RendererPopMatrix();
    void RendererRotate(double angle, double x, double y, double z);
    void RendererTranslate(double x, double y, double z);

    void RendererEndPolygon();

    bool RendererEnd();

    void RayColor(const CRay& p_ray, CRayColor& p_color, int p_recursive, const CRayIntersection::Object* p_ignore);


    

    struct PhongPair
    {
        float diffuse;
        float specular;
    };


    PhongPair BlinnPhong(CGrPoint lightDir, float lightInt, CGrPoint position, CGrPoint normal, float Ka, float Kd, float Ks, float shininess);


private:
    int m_rayimagewidth;
    int m_rayimageheight;
    BYTE** m_rayimage;
    CWnd* m_window;
    CRayIntersection m_intersection;
    std::list<CGrTransform> m_mstack;
    CGrMaterial* m_material;

};







